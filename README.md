# Orman Yangını Tespiti Drone Projesi

Bu proje, bir drone kullanarak ormanlarda yangın tespiti yapabilen bir sistem geliştirmeyi amaçlamaktadır. Sistem, Jetson Nano'ya bağlı bir Raspberry Pi V1 kamerası ile canlı görüntüleri işler ve Yolo modelini kullanarak yangın tespiti gerçekleştirir. Yangın tespit edildiğinde, sistem e-posta ile yangın fotoğrafı ve konum bilgisi gönderir.

---

## Proje Özeti
🎥 Demo Video: https://youtu.be/ZIup5u7ugtg?si=76OZGFrAjp-8RO1f 

Bu proje, drone tabanlı bir yangın tespit sistemi için geliştirilmiştir. Sistem, aşağıdaki işlevleri yerine getirir:

![IMG_20230728_190255](https://github.com/user-attachments/assets/6f16278f-dee7-47ae-afd0-81b86d9319a8)

* **Canlı Görüntü İşleme**: Raspberry Pi V1 kamerası ile video akışı alınır ve bu görüntüler üzerinde Yolo modeli kullanılarak yangın tespiti yapılır.
* **Yolo Tespiti**: Yolo (You Only Look Once) algoritması, görüntüdeki yangınları hızlı ve doğru bir şekilde tespit etmek için kullanılır.
* **E-posta Bildirimi**: Yangın tespit edildiğinde, yangın görüntüsü ve cihazın konum bilgisi içeren bir e-posta otomatik olarak gönderilir.
* **Raspberry Pi ile Entegrasyon**: Jetson Nano ve Raspberry Pi V1 Camera, bu sistemde kullanılan ana donanım bileşenleridir.

## Gereksinimler

* **Python 3.8**: Python'un 3.8 ve üzeri sürümler uyumludur.
* **OpenCV**: Görüntü işleme ve video akışını sağlamak için OpenCV kütüphanesi.
* **PyTorch ve YOLOv5**: Yolo modelinin çalışması için PyTorch ve YOLOv5 kullanılmaktadır.
* **SMPT Lib**: E-posta gönderimi için kullanılan kütüphane.
* **requests**: Konum bilgisini almak için kullanılan kütüphane.

### Kütüphaneler

Aşağıdaki kütüphanelerin yüklü olması gerekmektedir:

```bash
pip install opencv-python torch requests smtplib numpy
```
![IMG_20230727_182721](https://github.com/user-attachments/assets/42890d85-4b57-47e1-9604-2d70279b933a)


## Kurulum ve Çalıştırma

### 1. Proje Dosyalarını İndirme

Proje dosyasını bilgisayarınıza indirin veya GitHub üzerinden kopyalayın.

Gerekli kütüphaneleri indirin:
```bash
pip install -r requirements.txt
```

### 2. Yolo Modeli

Bu proje, yangın tespiti için eğitilmiş bir Yolo modeline ihtiyaç duyar. Repoda mevcut 3 farklı yolov5 modeli mevcuttur ancak kendi modelinizi kullanmak isterseniz kendi modelinizi `.pt` formatında edinin ve proje dizinine yerleştirin. Aşağıdaki kod satırını model yolunuza göre güncelleyin:

```python
model = torch.hub.load('ultralytics/yolov5', 'custom', path='fire_model.pt')
```
![IMG_20230726_104930](https://github.com/user-attachments/assets/4493ecdb-7c72-400c-99aa-88fa9a2a8372)

### 3. Donanım Kurulumu

Jetson Nano ve Raspberry Pi V1 kameranızı aşağıdaki adımları takip ederek bağlayın:

* Jetson Nano'yu kurun ve uygun yazılım sürümünü yükleyin.
* Raspberry Pi V1 kamerasını doğru bir şekilde bağladığınızdan emin olun.

### 4. Kamera Akışı

GStreamer pipeline'ı kullanarak kameradan video akışını alabilirsiniz. Raspberry Pi ve Jetson Nano için optimize edilmiş GStreamer pipeline'ı aşağıdaki gibi yapılandırılmıştır:

```python
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
```

### 5. Çalıştırma

Projeyi çalıştırmak için terminalde aşağıdaki komutu kullanın:

```bash
python3 yangin_tespiti.py
```
---

![fire_detected_image](https://github.com/user-attachments/assets/8e683bff-b507-41f8-b5b9-a0418703715e)

## Kullanım

* Proje çalışmaya başladığında, kamera görüntüsü canlı olarak gösterilecektir.
* Yangın tespiti yapıldığında, sistem e-posta ile yangın fotoğrafını ve konum bilgisini gönderecektir.
* Eğer yangın tespiti belirli bir sayıya (örneğin 50) ulaşırsa, e-posta gönderme işlemi otomatik olarak yapılacaktır.

### E-posta Ayarları

E-posta göndermek için aşağıdaki değişkenlerde yer alan e-posta adreslerini ve şifreyi güncelleyerek kendi hesap bilgilerinizi girmelisiniz:

```python
email_address = "your_email@hotmail.com"
password = "your_password"
to_email_address = "recipient_email@gmail.com"
```

### Konum Bilgisi

Proje, cihazın konum bilgisini `https://ipinfo.io/` servisi üzerinden alır ve yangın tespiti ile birlikte e-posta ile gönderir.

---

## 🧪 Demo Kullanımı — FİRE.mp4 Videosu ile Test

Projeyi kamera yerine videoyla denemek isterseniz, elinizdeki FİRE.mp4 dosyasını doğrudan kullanabilirsiniz:
ATES.mp4 dosyasının proje kök dizininde olduğundan emin olun (kodla aynı klasörde).
Kodda şu satırı bulun:

```bash
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
```
ve bu satırı aşağıdaki şekilde değiştirin:

```bash
cap = cv2.VideoCapture("FİRE.mp4")
```
Kodun geri kalan kısmını olduğu gibi bırakın; yani model yükleme, yangın tespiti, e‑posta gönderimi gibi mantık aynı şekilde çalışacaktır. 

![1711979356615](https://github.com/user-attachments/assets/977c0f9f-2691-45d6-90d8-ff829e95f06c)

Eğer pc de demo olarak denemek isterseniz:
```bash
cap = cv2.VideoCapture(0)
```
yazmanız yeterlidir.

---

## Proje Mimarisi

Projenin temel işleyişi şu şekildedir:

1. **Canlı Video Akışı**: Raspberry Pi V1 kamerası ile alınan video akışı üzerinde Yolo modelini kullanarak gerçek zamanlı yangın tespiti yapılır.
2. **Yangın Tespiti**: Yolo modeli, video akışındaki her bir kareyi analiz eder ve yangın tespit eder.
3. **E-posta Bildirimi**: Yangın tespit edilirse, sistem ilgili resmi ve konum bilgisini içeren bir e-posta gönderir.
4. **Veri Kaydetme**: Yangın tespit edildiğinde, sistem tespit edilen görüntüyü kaydeder.

## Proje Detayları

* **Yolo Modeli**: Yangın tespitini gerçekleştiren Yolo modeli, PyTorch kullanılarak eğitilmiştir. Modelin eğitiminde, yangınları tanımlayan veri kümesi kullanılmıştır.
* **E-posta Gönderimi**: Yangın tespiti sonrası, SMTP protokolü ile bir e-posta gönderimi yapılır. Bu işlem için `smtplib` kütüphanesi kullanılır.
* **Konum Bilgisi**: Cihazın konum bilgisi, IP adresine dayalı olarak `ipinfo.io` servisi kullanılarak alınır.
---

### Ekstra Bilgiler

* **Geliştirici**: [Fatih AYIBASAN] (Bilgisayar Mühendisliği Öğrencisi)
* **E-posta**: [fathaybasn@gmail.com]

---
