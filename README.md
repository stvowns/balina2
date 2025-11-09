# 🐋 Balina2Droid v2.1.1 - Enterprise-Grade Çoklu Cüzdan Kripto Takip Sistemi

> **5 dakikada kurulan, enterprise-grade kripto cüzdan takip sistemi** - Circuit Breaker, Async Processing ve Telegram bildirimleriyle anında değişimleri izleyin.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![Hyperliquid](https://img.shields.io/badge/Hyperliquid-Integrated-purple.svg)](https://hyperliquid.xyz/)

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

### 🔧 **3. Telegram Bot Kurulumu**
1. @BotFather ile konuşun → `/newbot` komutunu verin
2. Botunuza isim ve kullanıcı adı verin
3. Bot token'ını kopyalayın
4. `python3 get_chat_id.py` ile Chat ID'nizi alın

### ⚙️ **4. Konfigürasyon**
`.env` dosyasını düzenleyin:
```bash
# Telegram ayarları
TELEGRAM_BOT_TOKEN=BOT_TOKENINIZ
TELEGRAM_CHAT_ID=CHAT_IDINIZ

# Etherscan API
ETHERSCAN_API_KEY=ETHERSCAN_API_KEY

# Çoklu cüzdan desteği
WALLET_1_ADDRESS=0xCUZDAN_ADRESINIZ
WALLET_1_NAME=Cüzdan Adı
WALLET_1_ENABLED=true

WALLET_2_ADDRESS=0xDIGER_CUZDAN_ADRESI
WALLET_2_NAME=İkinci Cüzdan
WALLET_2_ENABLED=true
```

### 🎯 **5. Çalıştırma**
```bash
source venv/bin/activate
python3 main.py --list    # Cüzdanları listele
python3 main.py --check   # Test çalıştırması
python3 main.py            # Sürekli izleme
```

**✅ 5 dakikada çalışır!** 🎉

## ✨ **Özellikler**

### 🚀 **Çoklu Cüzdan Sistemi**
- **Sınırsız cüzdan desteği** - 100+ cüzdan takibi
- **Esnek konfigürasyon** - Wallet 1 ve 3, Wallet 2 olmadan çalışır
- **Per-wallet bildirimler** - Her cüzdan için özel Telegram/chat
- **Cüzdan yönetimi** - `WALLET_X_ENABLED=false` ile devre dışı bırakma

### ⚡ **Async Performans (v2.1)**
- **8x Hız Artışı** - 10+ wallet: 60s → 7.5s
- **Paralel API çağrıları** - Etherscan & Hyperliquid için eş zamanlı işlem
- **Rate Limiting** - API limit koruması (Etherscan: 5 req/s, Hyperliquid: 10 req/s)

### 🛡️ **Enterprise-Grade Güvenilirlik**
- **Circuit Breaker** - API failures'ı engelle, sistem devamlılığı
- **Intelligent Retry** - Exponential backoff with jitter
- **API Fallback** - V1/V2 Etherscan API otomatik geçiş
- **Graceful Degradation** - API sorunlarında bile bildirimler devam eder

### 🔥 **Gelişmiş Bildirimler**
- **Değişen pozisyon vurgulama** - `🔄 POSITION CHANGED - BTC` formatı
- **Tüm pozisyonlar** - Sınırsız pozisyon desteği (önceki 5 limiti kaldırıldı)
- **Finansal detaylar** - PnL, marj kullanımı, kaldıraç, account value
- **Multi-channel** - Console, Email, Telegram bildirimleri

## 🎯 **Bu Proje Ne İşe Yarar?**

### 💼 **Kimler İçin?**
- **Çoklu Cüzdan Kullanıcıları** - Birden fazla cüzdanı olanlar
- **Trader'lar** - Hyperliquid pozisyonlarını takip edenler
- **Yatırımcılar** - Portföy değerlerini izleyenler
- **Crypto Meraklıları** - Birden fazla cüzdanı tek yerden yönetmek isteyenler

### 📈 **Neler Takip Edilir?**
- **ETH Bakiyesi** - Giden/gelen transferler
- **ERC-20 Token'lar** - Tüm token transferleri (BTC, USDT, DOGE vb.)
- **Hyperliquid Pozisyonları** - Tüm pozisyonlar, PnL, marj kullanımı
- **Hesap Değeri** - Toplam portföy değeri ve değişimleri
- **Leverage ve Risk** - Kaldıraç oranları ve marj kullanımı

### 🔔 **Bildirimler Ne Zaman Gelir?**
- 📥 Para yatırma/çekme işlemleri
- 🚀 Pozisyon açılışı/kapanışı
- 🔄 Anlamlı bakiye değişiklikleri
- ✅ Tüm pozisyon değişimleri
- 🔥 **Değişen varlığı net belirtme** - Hangi coinin değiştiğini gösterme
- 💰 **PnL değişimleri** - Kar/zarar bildirimleri

## 📋 **Detaylı Yapılandırma**

### 📱 **Çoklu Cüzdan Ekleme**

**Tek Tek Ekleme (Önerilen):**
```bash
# Cüzdan 1
WALLET_1_ADDRESS=0xCUZDAN_ADRESINIZ
WALLET_1_NAME=Ana Cüzdan
WALLET_1_ENABLED=true

# Cüzdan 2 (devre dışı)
# WALLET_2_ADDRESS=0xDIGER_CUZDAN
# WALLET_2_NAME=Yedek Cüzdan
# WALLET_2_ENABLED=false

# Cüzdan 3 (aktif)
WALLET_3_ADDRESS=0xUCUNCUZDAN
WALLET_3_NAME=Trade Cüzdanı
WALLET_3_ENABLED=true
```

**JSON Formatı (İleri Düzey):**
```bash
WALLETS_JSON={"main":{"address":"0xCUZDAN1","name":"Ana Cüzdan","enabled":true},"backup":{"address":"0xCUZDAN2","name":"Yedek","enabled":false}}
```

### 📧 **E-posta Bildirimleri (İsteğe Bağlı)**

**⚠️ ÖNEMLİ:** E-posta bildirimleri default olarak kapalıdır. Aktifleştirmek için:

1. **Gmail App Password oluşturun:**
   - Google Account → Security → 2-Step Verification
   - App passwords → Mail için 16 haneli şifre oluşturun

2. **.env dosyasında aktifleştirin:**
```bash
EMAIL_SENDER=gmail@gmail.com
EMAIL_PASSWORD=16_HANELI_APP_PASSWORD
EMAIL_RECIPIENT=alerts@example.com
```

### 🎨 **Per-Wallet Özel Bildirimler**
Farklı Telegram chat'leri veya email alıcıları için:
```bash
# Ana Telegram chat ID
TELEGRAM_CHAT_ID=MAIN_CHAT_ID

# Wallet 2 için farklı chat
WALLET_2_TELEGRAM_CHAT_ID=WALLET_2_CHAT_ID

# Wallet 3 için farklı email
WALLET_3_EMAIL_RECIPIENT=wallet3@example.com
```

### ⚙️ **Ayar Seçenekleri**
```bash
CHECK_INTERVAL=600  # Kontrol sıklığı (saniye)
BALANCE_CHANGE_THRESHOLD=0.1  # ETH değişim uyarısı
POSITION_CHANGE_THRESHOLD=1000  # $1000 değişim uyarısı
```

## 🚀 **Kullanım**

### 📱 **Programı Çalıştırma**
```bash
source venv/bin/activate
python3 main.py            # Sürekli izleme
python3 main.py --check    # Tek kontrol yap
python3 main.py --list     # Cüzdanları listele
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

## 📂 **Dosya Yapısı**

```
balina2droid/
├── main.py                      # Ana program
├── config.py                    # Ayarlar ve validasyon
├── multi_wallet_tracker.py      # Çoklu cüzdan yönetimi
├── wallet_tracker.py            # Tek cüzdan takibi
├── notification_system.py       # Bildirim sistemi
├── position_formatter.py        # Pozisyon formatlama
├── logger_config.py             # Log yapılandırması
├── utils.py                     # Yardımcı fonksiyonlar
├── constants.py                 # Sabit değerler
├── install.sh                   # Kurulum scripti
├── requirements.txt             # Python paketleri
├── .env.example                 # Ayar şablonu
├── tests/                       # Test dosyaları
└── docs/                        # Dokümantasyon
```

## 🔧 **Sıkça Sorulan Sorular**

### 🎨 **Emoji Gösterim Sorunu**
**Sorun:** Telegram'da yeşil/kırmızı emojiler görünmüyor

**Çözüm:** Sistem otomatik olarak Telegram uyumlu emojiler kullanır:
- ✅ Pozitif PnL için
- ❌ Negatif PnL için
- ➖ Nöt durumlar için

### 🔥 **Pozisyon Vurgulama Özelliği**
**Sorun:** 10 varlık içinde hangisinde değişiklik olduğunu bulamama

**Çözüm:** Sistem değişen pozisyonu net belirtir:
- **Telegram Başlığı:** `🔄 POSITION CHANGED - ETH`
- **Telegram Listesi:** `🔥 ETH SHORT: -10 @ $3000` (diğerleri normal)

### 📱 **Boşluklu Wallet Konfigürasyonu**
**Sorun:** Wallet 1 ve Wallet 3 varken Wallet 2 olmadan sistem çalışmıyor

**Çözüm:** Yeni versiyon boşluklu konfigürasyonu destekler:
- ✅ `WALLET_1` ve `WALLET_3` aktif, `WALLET_2` yok
- ✅ `WALLET_1`, `WALLET_5`, `WALLET_10` gibi rastgele sıralama

### 🔄 **String-Int Karşılaştırma Hatası**
**Sorun:** `'>' not supported between instances of 'str' and 'int'`

**Çözüm:** Düzeltilmiş versiyonda bu hata artık oluşmaz:
- ✅ Güvenli numeric dönüşümleri
- ✅ Type-safe karşılaştırmalar
- ✅ Robust error handling

### 🔢 **Pozisyon Değeri $0 Gösteriyor**
**Sorun:** Total Position Value ve Unrealized PnL $0.00 görünüyor

**Çözüm:** v2.1'de düzeltilmiş Hyperliquid API alan eşleşmeleri:
- ✅ `totalNotion` → `totalNtlPos` (doğru API alanı)
- ✅ `unrealizedPnl` → individual pozisyonlardan toplanıyor
- ✅ `marginUsage` → `totalMarginUsed / accountValue` oranı
- ✅ Artık tüm değerler doğru gösteriliyor: Account Value, Total Position, PnL, Margin %

## ⚠️ **Güvenlik**

- 🔐 **API anahtarlarınızı asla paylaşmayın**
- ✅ **Cüzdan adresleri doğrulanır**
- 🚏 **API limitlerine dikkat edin**
- 📋 **.env dosyasını .gitignore'e ekleyin**
- 🛡️ **HTTPS API çağrıları kullanın**

## 🤝 **Katkıda Bulun**

1. **Fork** yapın
2. **Feature branch** oluşturun (`git checkout -b feature/AmazingFeature`)
3. **Commit** yapın (`git commit -m 'Add some AmazingFeature'`)
4. **Push** yapın (`git push origin feature/AmazingFeature`)
5. **Pull Request** açın

## 🗺️ **Yol Haritası**

### ✅ **Tamamlanan Özellikler (v2.1)**
- ⚡ **Circuit Breaker Pattern** - API failures'ı engelle
- 🔄 **Exponential Backoff Retry** - Akıllı yeniden deneme
- 🚨 **API Fallback** - V1/V2 Etherscan API otomatik geçiş
- ⏱️ **8x Performance Boost** - Async concurrent processing
- 🔧 **Hyperliquid API Fix** - Pozisyon değerleri ve PnL hesaplama düzeltmeleri

### 🤔 **Değerlendirilen Özellikler**
- **Caching System** - %70-80 API call reduction, cost savings
- **Multi-Blockchain** - Diğer blockchain'ler için destek
- **Mobile App** - React Native mobil uygulama
- **Advanced Analytics** - Pattern recognition ve anomaly detection

---

## 📄 **Lisans**

[MIT Lisansı](LICENSE)

---

<div align="center">

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

Made with ❤️ by [Balina2Droid Team](https://github.com/stvowns)

</div>