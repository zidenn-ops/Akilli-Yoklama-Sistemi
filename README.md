# 🚀 Akıllı Yoklama Sistemi (AI & Cloud Entegrasyonlu)

Bu proje, bir lise yazılım projesi olarak geliştirilmiş olup; yapay zeka ve bulut bilişim teknolojilerini bir araya getirerek okullarda yoklama sürecini otomatikleştirmeyi hedefler.

## ✨ Projenin Amacı ve Çalışma Mantığı
Sistem, bilgisayar kamerasından aldığı canlı görüntüyü anlık olarak işler. Derin öğrenme (Deep Learning) temelli bir model kullanarak öğrencilerin yüzlerini tanır ve isimlerini belirler. Belirlenen isimler, sistem tarafından tarih ve saat bilgisiyle birlikte bir `.csv` (Excel uyumlu) dosyasına kaydedilir.

### Öne Çıkan Özellikler:
- **Dinamik Bulut Güncelleme:** Model dosyaları (`.h5` ve `labels.txt`) doğrudan Google Drive üzerinden çekilir. Bu sayede yeni bir öğrenci eklemek için kodun değiştirilmesine gerek kalmaz.
- **Modern Arayüz:** Flask altyapısı kullanılarak oluşturulan Turkuaz Neon temalı dashboard üzerinden canlı takip yapılabilir.
- **Otomatik Veri Kaydı:** Tanınan her öğrenci, benzersiz bir şekilde yoklama listesine işlenir ve bu liste web üzerinden indirilebilir.

## 🛠️ Nelerden Yardım Alındı? (Teknolojiler)
Bu projeyi geliştirirken aşağıdaki kütüphane ve araçlardan faydalanılmıştır:
- **Python & Flask:** Uygulamanın ana iskeleti ve web sunucusu için.
- **TensorFlow & Keras:** Yapay zeka modelinin çalıştırılması ve tahminleme yapılması için.
- **OpenCV:** Kamera görüntüsünün işlenmesi ve yüz tespiti (Haar Cascade) için.
- **Teachable Machine:** Modelin eğitilmesi ve veri seti oluşturulması için.
- **Gdown:** Google Drive API entegrasyonu ve dosya senkronizasyonu için.

## 🚀 Nasıl Çalıştırılır?
1. Proje dosyalarını indirin.
2. Gerekli kütüphaneleri yükleyin: `pip install flask opencv-python tensorflow tf-keras gdown`.
3. `python3 app.py` komutuyla sistemi başlatın.
4. Tarayıcınızdan `http://localhost:5001` adresine gidin.

## 👨‍💻 Geliştirici
- **Deniz Yılmaz** - 11/A Yazılım Bölümü Öğrencisi