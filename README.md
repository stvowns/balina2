# 🐋 Balina2Droid - Çoklu Cüzdan Kripto Takip Sistemi

> **Gelişmiş kripto para cüzdanı izleme aracı** - Birden fazla Ethereum cüzdanını ve Hyperliquid pozisyonlarını aynı anda izleyen, önemli değişiklikler olduğunda Telegram üzerinden anlık bildirim gönderen Python uygulaması.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)

## ✨ Özellikler

- 🚀 **Çoklu Cüzdan Desteği** - Aynı anda sınırsız sayıda cüzdanı izleme
- 📱 **Cüzdan Bazlı Bildirimler** - Her cüzdan için ayrı Telegram/Email bildirim ayarları
- 📊 **Akıllı İzleme** - Sadece önemli olaylar için bildirim (gürültü yok)
- 🔔 **Gerçek Zamanlı Bildirimler** - Pozisyon değişiklikleri ve transferler için anlık bildirim
- ⚙️ **Esnek Konfigürasyon** - JSON, environment variables veya tek cüzdan desteği
- 🛡️ **Güvenli Yapılandırma** - Şifreli ve doğrulanmış konfigürasyon yönetimi
- 🧪 **Test Kapsamı** - Kapsamlı birim test desteği
- 🔄 **Backward Compatibility** - Mevcut tek cüzdan yapılandırmalarıyla tam uyumlu

## 🎯 Bu Proje Ne İşe Yarar?

Balina2Droid, kripto para yatırımcılarının ve trader'ların birden fazla cüzdanını tek bir yerden takip etmesini sağlayan profesyonel bir izleme aracıdır:

### 💼 Kimler İçin Uygun?
- **Çoklu Cüzdan Kullanıcıları** - Farklı amaçlar için birden fazla cüzdanı olanlar
- **Trader'lar** - Hyperliquid pozisyonlarını aktif olarak takip edenler
- **Yatırımcılar** - Portföy değerlerini ve hareketlerini izlemek isteyenler
- **Hesap Yöneticileri** - Müşteri cüzdanlarını izleyenler

### 📈 Neler Takip Edilir?
- **ETH Bakiyesi** - Gelen/giden ETH transferleri
- **ERC-20 Token'lar** - Tüm token transferleri (BTC, USDT vb.)
- **Hyperliquid Pozisyonları** - Açık/kapalı pozisyonlar, PnL, marj kullanımı
- **Hesap Değeri** - Toplam portföy değeri ve değişimleri

### 🔔 Hangi Durumlarda Bildirim Gelir?
- 📥 **Para Yatırma** - Cüzdana ETH veya token geldiğinde
- 📤 **Para Çekme** - Cüzdan para gönderdiğinde
- 🚀 **Pozisyon Açıldı** - Yeni pozisyon oluşturulduğunda
- ✅ **Pozisyon Kapandı** - Pozisyon kapatıldığında
- 🔄 **Pozisyon Değişti** - Anlamlı pozisyon değişikliklerinde
- 💰 **Bakiye Değişimi** - Anlamlı ETH bakiye değişikliklerinde

## 🏗️ Konfigürasyon Yöntemleri

Balina2Droid 3 farklı konfigürasyon yöntemi sunar:

### 🥇 **Yöntem 1: Individual Environment Variables (Önerilen)**
- ✅ **Kullanıcı Dostu** - Her ayar ayrı satırda, kolay yönetim
- ✅ **Kopyala-Yapıştır** - Yeni cüzdan eklemek çok basit
- ✅ **Anlaşılır** - JSON formatının karmaşıklığı yok
- ⭐ **Yeni Başlayanlar İçin İdeal**

### 🥈 **Yöntem 2: JSON Konfigürasyonu (İleri Düzey)**
- 📦 **Tek Satırda** - Tüm cüzdanlar bir JSON objesinde
- 🔧 **Gelişmiş** - Karmaşık yapılar için esnek
- ⚡ **Hızlı** - Tek komutla tüm cüzdanlar
- 🎯 **Teknik Kullanıcılar İçin**

### 🥉 **Yöntem 3: Tek Cüzdan (Backward)**
- 🔄 **Mevcut Uyum** - Eski tek cüzdan sistemleriyle uyumlu
- 📝 **Basit** - Sadece bir cüzdan için minimal ayar
- 🔄 **Geçiş** - Multi-wallet'a geçiş için köprü

## 📋 Kurulum

### 🔧 Gereksinimler
- Python 3.7+
- Telegram hesabı (bot oluşturmak için)
- Etherscan API anahtarı

### 1. Depoyu Klonlama
```bash
git clone https://github.com/stvowns/balina2.git
cd balina2droid
```

### 2. Kurulum (2 Seçenek)

#### 🚀 Otomatik Kurulum (Önerilen)
Kurulum script'i tüm adımları sizin için yapar:
```bash
chmod +x install.sh
./install.sh
```

#### 🔧 Manuel Kurulum
Script'in yaptığı adımları manuel olarak takip etmek için:
```bash
# 1. Python'ın yüklü olduğunu kontrol edin
python3 --version

# 2. Sanal ortam oluşturun (eğer mevcut değilse)
python3 -m venv venv

# 3. Sanal ortamı aktifleştirin
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# 4. .env dosyasını oluşturun
cp .env.example .env

# 5. pip'ı güncelleyin ve bağımlılıkları yükleyin
pip install --upgrade pip
pip install -r requirements.txt

# 6. Kurulumu tamamladığınızda kontrol edin
nano .env  # Yapılandırmanızı düzenleyin
python3 main.py --list
```

## ⚙️ 4. Çoklu Cüzdan Yapılandırması

### 📱 1. Telegram Bot Oluşturma
1. Telegram'da **[@BotFather](https://t.me/botfather)** ile konuşun
2. `/newbot` komutunu verin
3. Botunuza bir isim ve kullanıcı adı verin
4. Bot token'ını kopyalayın (güvenli bir yerde saklayın)

### 🔑 2. Chat ID Öğrenme
```bash
python3 telegram_utilities.py
```
Bot token'ı girip botunuza mesaj gönderin, chat ID'nizi alacaksınız.

### 🏗️ 5. Çoklu Cüzdan Konfigürasyonu

#### Yöntem 1: Individual Environment Variables (Önerilen)
`.env` dosyasına aşağıdakileri ekleyin:
```bash
# Cüzdan 1 - Trading Wallet
WALLET_1_ADDRESS=0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45
WALLET_1_NAME=Trading Wallet
WALLET_1_ENABLED=true
# WALLET_1_TELEGRAM_CHAT_ID=123456789  # Sadece farklı chat ID kullanılacaksa

# Cüzdan 2 - Savings Wallet
WALLET_2_ADDRESS=0x1234567890123456789012345678901234567890
WALLET_2_NAME=Savings Wallet
WALLET_2_ENABLED=false

# API anahtarı (zorunlu)
ETHERSCAN_API_KEY=SIZIN_ETHERSCAN_API_KEY

# Global Telegram ayarları
TELEGRAM_BOT_TOKEN=BOT_TOKENINIZ
TELEGRAM_CHAT_ID=GLOBAL_CHAT_ID
```

#### Yöntem 2: JSON Konfigürasyonu (İleri Düzey Kullanıcılar)
```bash
# API anahtarı (zorunlu)
ETHERSCAN_API_KEY=SIZIN_ETHERSCAN_API_KEY

# Global Telegram ayarları
TELEGRAM_BOT_TOKEN=BOT_TOKENINIZ
TELEGRAM_CHAT_ID=GLOBAL_CHAT_ID

# Tüm cüzdanlar JSON formatında
WALLETS_JSON={"trading":{"address":"0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45","name":"Trading Wallet","enabled":true,"telegram_chat_id":"123456789"},"savings":{"address":"0x1234567890123456789012345678901234567890","name":"Savings Wallet","enabled":false}}
```

#### Yöntem 3: Tek Cüzdan (Backward Compatibility)
```bash
WALLET_ADDRESS=0xSINGLE_WALLET_ADDRESS
ETHERSCAN_API_KEY=SIZIN_ETHERSCAN_API_KEY
TELEGRAM_BOT_TOKEN=BOT_TOKENINIZ
TELEGRAM_CHAT_ID=CHAT_ID
```

### 📧 6. E-posta Bildirimleri (İsteğe Bağlı)

E-posta bildirimlerini aktifleştirmek için Gmail App Password oluşturmanız gerekir:

#### 🔒 Gmail App Password Oluşturma
1. **Google Hesabınızda**: Account → Security → 2-Step Verification
2. **2-Step Verification'i aktifleştirin**
3. **App passwords seçeneğine tıklayın**
4. **"Mail" için app password oluşturun** (16 haneli şifre)
5. **Bu şifreyi kopyalayın** - normal Gmail şifrenizi KULLANMAYIN!

#### 📧 E-posta Konfigürasyonu
```bash
# E-posta gönderen hesap (Gmail önerilir)
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop  # 16 haneli App Password
EMAIL_RECIPIENT=alerts@example.com    # Bildirim alacak e-posta
```

#### 🎯 E-posta Bildirim Seçenekleri

**Seçenek 1 - Global E-posta (Tüm cüzdanlar için aynı):**
```bash
EMAIL_SENDER=tracker@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
EMAIL_RECIPIENT=alerts@example.com
# Sonuç: Tüm cüzdan bildirimleri alerts@example.com'e gider
```

**Seçenek 2 - Cüzdan Bazlı E-posta:**
```bash
# Global e-posta (fallback)
EMAIL_SENDER=tracker@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
EMAIL_RECIPIENT=default@example.com

# Cüzdan 1 için özel e-posta
WALLET_1_EMAIL_RECIPIENT=trading@example.com

# Cüzdan 2 için özel e-posta
WALLET_2_EMAIL_RECIPIENT=savings@example.com
# Sonuç: Her cüzdan farklı e-postaya bildirim gönderir
```

#### ⚙️ Desteklenen E-posta Sağlayıcıları
- ✅ **Gmail** (App Password ile - önerilir)
- ✅ **Outlook/Hotmail**
- ✅ **Yahoo Mail**
- ✅ **Corporate SMTP** (özel SMTP ayarları ile)

#### 🔄 Aç/Kapat İşlemi
- **Açmak için**: `#` işaretlerini kaldırın ve bilgileri doldurun
- **Kapatmak için**: `#` işaretleri ekleyin veya satırları silin
- **Sadece Telegram**: E-posta ayarlarını boş bırakın

### ⚡ 7. İleri Seviye Yapılandırma
```bash
# Kontrol sıklığı (saniye)
CHECK_INTERVAL=600  # 10 dakika

# Bildirim eşikleri
BALANCE_CHANGE_THRESHOLD=0.1  # 0.1 ETH
POSITION_CHANGE_THRESHOLD=1000  # $1000
```

## 🚀 Kullanım

### 🔔 Bildirim Durumu Kontrolü
Önce bildirim ayarlarınızın doğru çalışıp çalışmadığını kontrol edin:
```bash
python3 main.py --list
```
Çıktıda şu bilgileri göreceksiniz:
- 📧 Email notifications: Enabled/Disabled
- 📱 Telegram notifications: Enabled/Disabled

### 📋 Cüzdanları Listeleme
Yapılandırılmış tüm cüzdanları ve durumlarını gösterir:
```bash
python3 main.py --list
```

### 🔍 Manuel Kontrol
Tüm cüzdanları bir kez kontrol eder ve durum raporu gösterir:
```bash
python3 main.py --check
```

### 🔄 Sürekli İzleme
Arka planda sürekli izleme başlatır:
```bash
python3 main.py
```

### 🧪 Testleri Çalıştırma
```bash
# Tüm testler
python3 test_runner.py

# Sadece çoklu cüzdan testleri
python3 test_runner.py --multi
```

## 📊 CLI Parametreleri Detayı

| Komut | Açıklama | Kullanım Alanı |
|-------|----------|---------------|
| `python3 main.py --check` | ✅ **Manuel Kontrol** - Tüm cüzdanları bir kez kontrol eder, detaylı rapor gösterir | Hızlı durum kontrolü, test amaçlı |
| `python3 main.py --list` | 📱 **Cüzdan Listesi** - Tüm yapılandırılmış cüzdanları ve ayarlarını listeler | Yapılandırma doğrulama |
| `python3 main.py` | 🔄 **Sürekli İzleme** - Arka planda otomatik kontrol ve bildirim | Üretim kullanımı |

## 🔧 Yapılandırma Seçenekleri

### 🏷️ Cüzdan Yönetimi
```bash
# Cüzdanları etkinleştirme/devre dışı bırakma
WALLET_1_ENABLED=true
WALLET_2_ENABLED=false

# Cüzdanlara özel isimler
WALLET_1_NAME=Ana Cüzdan
WALLET_2_NAME=Yedekleme Cüzdan
```

### ⚖️ Kontrol ve Eşikler
```bash
# Kontrol sıklığı
CHECK_INTERVAL=300  # 5 dakika

# Bildirim eşikleri
BALANCE_CHANGE_THRESHOLD=0.05  # 0.05 ETH
POSITION_CHANGE_THRESHOLD=500   # $500
```

## 📁 Proje Yapısı

```
balina2droid/
├── main.py                    # Ana uygulama ve CLI arayüzü
├── multi_wallet_tracker.py    # Çoklu cüzdan yönetimi
├── wallet_tracker.py          # Tekil cüzdan takip işlemleri
├── notification_system.py     # Bildirim sistemi
├── config.py                  # Konfigürasyon yönetimi
├── utils.py                   # Yardımcı fonksiyonlar
├── test_*.py                  # Test dosyaları
├── .env.example               # Konfigürasyon şablonu
├── requirements.txt           # Python bağımlılıkları
├── install.sh                 # Kurulum scripti
└── README.md                  # Bu dosya
```

## 🔧 Test ve Hata Ayıklama

### 📱 Telegram Bağlantısı Testi
```bash
python3 telegram_utilities.py
```

### 🔍 Cüzdan Durumu Kontrolü
```bash
python3 debug_positions.py
```

### 🧪 Çoklu Cüzdan Testleri
```bash
python3 test_multi_wallet.py
```

## ⚠️ Güvenlik Notları

- **🔐 HASSAS BİLGİLER**: API anahtarları ve özel bilgiler asla paylaşmayın
- **✅ KONFİGÜRASYON GÜVENLİĞİ**: Cüzdan adresleri ve formatları doğrulanır
- **🚏 API LİMİTLERİ**: Etherscan API kullanım limitlerine dikkat edin
- **🔒 ŞİFRELİ SAKLAMA**: Hassas bilgiler için güvenli saklama yöntemleri kullanın

## 🤝 Katkıda Bulunma

Katkıda bulunmak isterseniz:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## 🔗 Faydalı Linkler

- [Etherscan API](https://etherscan.io/apis) - API anahtarı almak için
- [Hyperliquid](https://hyperliquid.xyz/) - Pozisyon takibi için
- [Telegram Bot API](https://core.telegram.org/bots) - Bot oluşturma için
- [Python](https://www.python.org/) - Python indir ve kur

## 📞 Destek

Sorunlaşırsanız veya sorunuz olursa:
1. [Issues](https://github.com/stvowns/balina2/issues) sayfasını kontrol edin
2. Yeni issue oluşturun
3. Toplulukla iletişime geçin

---

<div align="center">

**⭐ Eğer projeyi beğendiyseniz yıldız vermeyi unutmayın!**

Made with ❤️ by [Balina2Droid Team](https://github.com/stvowns)

</div>