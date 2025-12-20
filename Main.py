import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import cv2
import numpy as np
import tf_keras as keras
from datetime import datetime

# --- AYARLAR ---
MODEL_PATH = "keras_model.h5"
LABELS_PATH = "labels.txt"
CONFIDENCE_THRESHOLD = 0.70 

# 1. Excel (CSV) Dosyasını Hazırla
if not os.path.exists("yoklama.csv"):
    with open("yoklama.csv", "w", encoding="utf-8") as f:
        f.write("OGRENCI ISMI;TARIH;SAAT;DURUM\n")

# Yüz bulucu ve Modeli yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = keras.models.load_model(MODEL_PATH, compile=False)
class_names = [line.strip() for line in open(LABELS_PATH, "r").readlines()]

# Kayıt tutucular
yoklama_dosya_kaydi = set()
ekrandaki_liste = {}

cap = cv2.VideoCapture(0)

win_name = "11/A Yazilim - Deniz Yilmaz - Yoklama"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret: break

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

        if confidence > CONFIDENCE_THRESHOLD and name != "Background":
            # Kişi görüldüğü an zamanını güncelle
            ekrandaki_liste[name] = mevcut_zaman 

            if name not in yoklama_dosya_kaydi:
                tarih = mevcut_zaman.strftime('%d.%m.%Y')
                saat = mevcut_zaman.strftime('%H:%M:%S')
                with open("yoklama.csv", "a", encoding="utf-8") as f:
                    f.write(f"{name};{tarih};{saat};GELDI\n")
                yoklama_dosya_kaydi.add(name)

    # --- LİSTE TEMİZLEME VE ÇİZİM ---
    ekran_g = frame.shape[1]
    cv2.putText(frame, "ANLIK BURADA OLANLAR", (ekran_g - 180, 25), 
                cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)
    
    y_pos = 50
    
    # Listeyi kopyalayarak üzerinde dönüyoruz (Runtime error almamak için)
    for kisi in list(ekrandaki_liste.keys()):
        son_gorulme = ekrandaki_liste[kisi]
        saniye_farki = (mevcut_zaman - son_gorulme).total_seconds()
        
        # 3 saniyeden uzun süredir görülmüyorsa listeden sil
        if saniye_farki > 3.0:
            del ekrandaki_liste[kisi]
        else:
            # Sadece hala orada olanları yazdır
            cv2.putText(frame, f"- {kisi[:15]}", (ekran_g - 170, y_pos), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            y_pos += 25

    cv2.imshow(win_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()