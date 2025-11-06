# 🐋 Balina2Droid - Çoklu Cüzdan Kripto Takip Sistemi

> **5 dakikada kurulan, profesyonel kripto cüzdan takip sistemi** - Telegram bildirimleriyle anında değişimleri izleyin.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)

## ⚡ **Hızlı Başlangıç (5 Dakika)**

### 📂 **1. Depoyu Klonlama**
```bash
git clone https://github.com/stvowns/balina2.git
cd balina2droid
```

### 🚀 **2. Otomatik Kurulum (Önerilen)**
```bash
chmod +x install.sh
./install.sh
```
**Script otomatik olarak:**
- ✅ Python kontrolü yapar
- ✅ Sanal ortam oluşturur
- ✅ Gerekli paketleri kurar
- ✅ `.env.example` dosyasını kopyalar

### 🔧 **3. Manuel Kurulum (İsteğe Bağlı)**
```bash
# Sanal ortam oluşturma
python3 -m venv venv

# Ortamı aktifleştirme
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Paketleri kurma
pip install -r requirements.txt

# Konfigürasyon dosyası
cp .env.example .env
```

### 🤖 **4. Telegram Bot Kurulumu (Zorunlu)**
```bash
# 1. BotFather ile konuşun
# 2. /newbot komutunu verin
# 3. Botunuza isim ve kullanıcı adı verin
# 4. Bot token'ını kopyalayın
```

### 🔑 **5. Chat ID Alma**
```bash
python3 get_chat_id.py
# Bot token'ı girin ve botunuza mesaj gönderin
# Chat ID'nizi kopyalayın
# Bazen ilk denemede hata verebilir. Tekrar deneyin.
```

### ⚙️ **6. Konfigürasyon**
`.env` dosyasını düzenleyin:
```bash
# Telegram ayarları
TELEGRAM_BOT_TOKEN=BOT_TOKENINIZ
TELEGRAM_CHAT_ID=CHAT_IDINIZ

# Etherscan API
ETHERSCAN_API_KEY=ETHERSCAN_API_KEY

# Cüzdan bilgileri
WALLET_1_ADDRESS=0xCUZDAN_ADRESINIZ
WALLET_1_NAME=Cüzdan Adı
WALLET_1_ENABLED=true
```

### 🎯 **7. Test ve Başlatma**
```bash
source venv/bin/activate
python3 main.py --check  # Test çalıştırması
python3 main.py         # Sürekli izleme
```

**✅ 5 dakikada çalışır!** 🎉

## ✨ Özellikler

- 🚀 **Çoklu Cüzdan Desteği** - Sınırsız cüzdanı aynı anda izleme
- 📱 **Cüzdan Bazlı Bildirimler** - Her cüzdan için ayrı bildirim ayarları
- 📊 **Akıllı İzleme** - Sadece önemli olaylar için bildirim
- 🔔 **Gerçek Zamanlı Bildirimler** - Transfer ve pozisyon değişiklikleri
- ⚙️ **Esnek Konfigürasyon** - JSON, environment variables, tek cüzdan desteği
- 🛡️ **Güvenli Yapılandırma** - Doğrulanmış adres ve API yönetimi
- 🧪 **Test Kapsamı** - Kapsamlı birim test desteği
- 🔄 **Backward Compatibility** - Mevcut yapılandırmalarla tam uyumlu

## 🎯 Bu Proje Ne İşe Yarar?

### 💼 Kimler İçin?
- **Çoklu Cüzdan Kullanıcıları** - Birden fazla cüzdanı olanlar
- **Trader'lar** - Hyperliquid pozisyonlarını takip edenler
- **Yatırımcılar** - Portföy değerlerini izleyenler

### 📈 Neler Takip Edilir?
- **ETH Bakiyesi** - Giden/giden transferler
- **ERC-20 Token'lar** - Tüm token transferleri (BTC, USDT vb.)
- **Hyperliquid Pozisyonları** - Tüm pozisyonlar (sınırsız), PnL, marj kullanımı
- **Hesap Değeri** - Toplam portföy değeri ve değişimleri

### 🔔 Bildirimler Ne Zaman Gelir?
- 📥 Para yatırma/çekme işlemleri
- 🚀 Pozisyon açılışı/kapanışı
- 🔄 Anlamlı bakiye değişiklikleri
- ✅ Tüm pozisyon değişimleri (sınırsız sayıda)

## 📋 Detaylı Yapılandırma

### 📱 Çoklu Cüzdan Ekleme

#### **Yöntem 1: Tek Tek Ekleme (Önerilen)**
```bash
# Cüzdan 1
WALLET_1_ADDRESS=0xCUZDAN_ADRESINIZ
WALLET_1_NAME=Ana Cüzdan
WALLET_1_ENABLED=true

# Cüzdan 2
WALLET_2_ADDRESS=0xDIGER_CUZDAN
WALLET_2_NAME=Yedek Cüzdan
WALLET_2_ENABLED=true

# API ayarları
ETHERSCAN_API_KEY=API_ANAHTARINIZ
TELEGRAM_BOT_TOKEN=BOT_TOKENINIZ
TELEGRAM_CHAT_ID=CHAT_IDINIZ
```

#### **Yöntem 2: JSON Formatı (İleri Düzey)**
```bash
WALLETS_JSON={"main":{"address":"0xCUZDAN1","name":"Ana Cüzdan","enabled":true},"backup":{"address":"0xCUZDAN2","name":"Yedek","enabled":false}}
```

### 📧 E-posta Bildirimleri (İsteğe Bağlı - Kapalı)

**⚠️ ÖNEMLİ:** E-posta bildirimleri **default olarak kapalıdır**.
Bu, Gmail authentication hatalarını önlemek içindir. Aktifleştirmek için:

#### 🔒 Gmail App Password Oluşturma
1. **Google Account** → Security → 2-Step Verification
2. **App passwords** → Mail için 16 haneli şifre oluşturun
3. **Bu şifreyi kopyalayın** - Normal Gmail şifrenizi KULLANMAYIN!

#### ⚙️ E-posta Aktifleştirme Adımları
`.env` dosyasında şu adımları izleyin:

1. **Tüm satırların uncomment'ını kaldırın** (başlarındaki # silin)
2. **EMAIL_ENABLED=true** yapın
3. **Bilgilerinizi girin**

```bash
# Email Configuration (Optional - Default DISABLED to prevent authentication errors)
EMAIL_ENABLED=true  # E-postayı aktifleştir
EMAIL_SENDER=gmail@gmail.com
EMAIL_PASSWORD=16_HANELI_APP_PASSWORD  # Gmail App Password kullanın
EMAIL_RECIPIENT=alerts@example.com
```

### ⚙️ Ayar Seçenekleri
```bash
CHECK_INTERVAL=600  # Kontrol sıklığı (saniye)
BALANCE_CHANGE_THRESHOLD=0.1  # ETH değişim uyarısı
POSITION_CHANGE_THRESHOLD=1000  # $1000 değişim uyarısı
```

## 🚀 Kullanım

### 📱 **Programı Çalıştırma**
```bash
source venv/bin/activate
python3 main.py           # Sürekli izleme
python3 main.py --check   # Tek kontrol yap
python3 main.py --list    # Cüzdanları listele
```

### 🧪 **Test Etme**
```bash
python3 test_runner.py    # Tüm testleri çalıştır
```

### ⚙️ **Cüzdan Yönetimi**
```bash
# Cüzdanı aç/kapa
WALLET_1_ENABLED=true     # Açık
WALLET_2_ENABLED=false    # Kapalı

# Cüzdan isimlerini değiştir
WALLET_1_NAME=Trade Cüzdanı
WALLET_2_NAME=Yedek Cüzdan
```

## 📂 Dosya Yapısı

```
balina2droid/
├── main.py              # Ana program
├── config.py            # Ayarlar
├── notification_system.py  # Bildirimler
├── wallet_tracker.py    # Cüzdan takibi
├── install.sh           # Kurulum scripti
├── requirements.txt     # Python paketleri
└── .env.example         # Ayar şablonu
```

## 🔧 Hata Çözümü

### 📱 Telegram Test
```bash
python3 get_chat_id.py  # Bot bağlantısını test et
```

### 🔍 Cüzdan Kontrolü
```bash
python3 main.py --check  # Cüzdanları kontrol et
```

### 🎨 Emoji Gösterim Sorunu
**Sorun:** Telegram'da yeşil/kırmızı emojiler görünmüyor

**Çözüm:** Sistem otomatik olarak Telegram uyumlu emojiler kullanır:
- ✅ Pozitif PnL için
- ❌ Negatif PnL için
- ➖ Nöt durumlar için

### 📊 Pozisyon Limiti
**Önceki durum:** Sadece ilk 5 pozisyon gösteriliyordu
**Yeni durum:** Tüm pozisyonlar sınırsız olarak gösterilir

## ⚠️ Güvenlik

- 🔐 **API anahtarlarınızı asla paylaşmayın**
- ✅ **Cüzdan adresleri doğrulanır**
- 🚏 **API limitlerine dikkat edin**

## 📄 Lisans

[MIT Lisansı](LICENSE)

---

<div align="center">

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

Made with ❤️ by [Balina2Droid Team](https://github.com/stvowns)

</div>