# AI-Powered Attendance System (Yapay Zeka Destekli Akıllı Yoklama Sistemi) 🚀

Bu proje, Python ve Derin Öğrenme (Deep Learning) teknikleri kullanılarak geliştirilmiş, gerçek zamanlı bir yoklama takip sistemidir.

## 🌟 Özellikler (Features)
- **Çoklu Yüz Tanıma:** Aynı anda birden fazla kişiyi tespit edebilir.
- **Anlık Varlık Takibi:** Kameradan ayrılan kişiler 3 saniye içinde listeden otomatik olarak silinir.
- **Excel Entegrasyonu:** Tanınan kişileri tarih ve saat damgasıyla `yoklama.csv` dosyasına kaydeder.
- **Minimalist HUD Arayüzü:** VGA kameralar için optimize edilmiş, ekranı kaplamayan şeffaf bilgi paneli.
- **Yüksek Performans:** Görüntü işleme süreçleri OpenCV ve TensorFlow kullanılarak optimize edilmiştir.

## 🛠️ Kullanılan Teknolojiler (Tech Stack)
- **Python 3.x**
- **OpenCV:** Görüntü işleme ve yüz tespiti (Haar Cascade).
- **TensorFlow / Keras:** Derin öğrenme model tahmini.
- **Google Teachable Machine:** Model eğitimi.
- **Gemini AI:** Yazılım mimarisi ve kod optimizasyonu desteği.

## 🚀 Kurulum (Setup)
1. Python 3.12 Sürümünü Kurunuz
2. Gerekli Kütüphaneleri Terminal Veya CMD Aracılığı ile kurunuz
    pip install opencv-python numpy tf_keras tensorflow
3. Tanınmasını istediğiniz yüzleri [Teachable Machine](https://teachablemachine.withgoogle.com) sitesinden Get started > Image Project kısmına Kişileri tek tek tanıtıp train model dedikten sonra export model ile "TensorFlow" seçeneğini seçip export aldıktan sonra "keras_model.h5" ve "labels.txt" dosyalarını ana dosyadakiler ile değiştiriyoruz
4. Terminale python main.py yazıyoruz ve işlem bu kadar programımız calısıyor