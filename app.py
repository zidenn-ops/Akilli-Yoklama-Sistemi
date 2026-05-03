import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

from flask import Flask, render_template, Response, send_file
import cv2
import numpy as np
import tf_keras as keras
from datetime import datetime
import gdown

app = Flask(__name__)

# --- 1. AYARLAR ---
MODEL_FILE_ID = '1QPWB87O7a_znabbZLE4BgfrbpThFDi3h'    #Drive idleri buraya gelicek
LABELS_FILE_ID = '12IhKr2p8_xdbBlXTp2m82Sw4DC_AHPZ4'
MODEL_PATH = "keras_model.h5"
LABELS_PATH = "labels.txt"
CSV_PATH = "yoklama.csv"
TURKUAZ_BGR = (255, 242, 0)

# Drive Güncelleme
def drive_dan_guncelle():
    try:
        gdown.download(f'https://drive.google.com/uc?id={MODEL_FILE_ID}', MODEL_PATH, quiet=True)
        gdown.download(f'https://drive.google.com/uc?id={LABELS_FILE_ID}', LABELS_PATH, quiet=True)
        print(">> Dosyalar Drive'dan güncellendi.")
    except:
        print(">> Drive bağlantısı kurulamadı, yerel dosyalarla devam ediliyor.")

drive_dan_guncelle()

# Model ve Dosya Hazırlığı
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write("OGRENCI ISMI;TARIH;SAAT;DURUM\n")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = keras.models.load_model(MODEL_PATH, compile=False)
class_names = [line.strip() for line in open(LABELS_PATH, "r").readlines()]

yoklama_dosya_kaydi = set()
ekrandaki_liste = {}

# --- 2. VİDEO AKIŞI ---
def gen_frames():
    cap = cv2.VideoCapture(0)
    # Mac Mini için çözünürlüğü sabitlemek akışı rahatlatabilir
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 6, minSize=(60, 60))
        mevcut_zaman = datetime.now()

        for (x, y, w, h) in faces:
            yuz_kesit = frame[y:y+h, x:x+w]
            yuz_hazir = cv2.resize(yuz_kesit, (224, 224))
            img_array = np.asarray(yuz_hazir, dtype=np.float32).reshape(1, 224, 224, 3)
            img_array = (img_array / 127.5) - 1

            prediction = model.predict(img_array, verbose=0)
            index = np.argmax(prediction)
            confidence = prediction[0][index]
            
            full_label = class_names[index]
            name = full_label.split(' ', 1)[-1] if ' ' in full_label else full_label

            if confidence > 0.70 and name != "Background":
                ekrandaki_liste[name] = mevcut_zaman 
                if name not in yoklama_dosya_kaydi:
                    with open(CSV_PATH, "a", encoding="utf-8") as f:
                        f.write(f"{name};{mevcut_zaman.strftime('%d.%m.%Y')};{mevcut_zaman.strftime('%H:%M:%S')};GELDI\n")
                    yoklama_dosya_kaydi.add(name)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), TURKUAZ_BGR, 2)
            cv2.putText(frame, f"%{int(confidence*100)}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, TURKUAZ_BGR, 1)

        # Liste Çizimi
        y_pos = 60
        for kisi in list(ekrandaki_liste.keys()):
            if (mevcut_zaman - ekrandaki_liste[kisi]).total_seconds() > 3.0:
                del ekrandaki_liste[kisi]
            else:
                cv2.putText(frame, f"> {kisi[:15]}", (frame.shape[1] - 140, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, TURKUAZ_BGR, 1)
                y_pos += 25

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# --- 3. YOLLAR (ROUTES) ---

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Zidenn AI Yoklama</title>
            <style>
                body { background: #0b1016; color: #00f2ff; font-family: sans-serif; text-align: center; padding: 20px; }
                .vid-box { border: 3px solid #00f2ff; border-radius: 15px; box-shadow: 0 0 30px rgba(0, 242, 255, 0.4); background: #000; display: inline-block; }
                .btn { 
                    background: #00f2ff; color: #0b1016; padding: 12px 25px; border: none; border-radius: 5px; 
                    font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 20px;
                    transition: 0.3s;
                }
                .btn:hover { background: #ffffff; box-shadow: 0 0 15px #00f2ff; }
                h1 { text-shadow: 0 0 10px #00f2ff; }
            </style>
        </head>
        <body>
            <h1>AKILLI YOKLAMA SISTEMI</h1>
            <div class="vid-box">
                <img src="/video_feed" width="750">
            </div>
            <br>
            <a href="/indir" class="btn">YOKLAMA LISTESINI INDIR (.CSV)</a>
        </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/indir')
def indir():
    return send_file(CSV_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)