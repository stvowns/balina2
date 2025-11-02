# Balina2Droid - Çoklu Cüzdan Kripto Takip Sistemi

Birden fazla Ethereum cüzdanını ve Hyperliquid pozisyonlarını aynı anda izleyen, değişiklikler olduğunda Telegram üzerinden bildirim gönderen Python uygulaması.

## 🚀 Özellikler

- **🚀 Çoklu Cüzdan Desteği**: Aynı anda birden fazla cüzdanı izleme
- **📱 Cüzdan Bazlı Bildirimler**: Her cüzdan için ayrı Telegram/Email bildirim ayarları
- **📊 Akıllı İzleme**: Sadece önemli olaylar için bildirim
- **🔔 Gerçek Zamanlı Bildirimler**: Pozisyon değişiklikleri ve transferler için anlık bildirim
- **⚙️ Esnek Konfigürasyon**: JSON, env vars veya tek cüzdan desteği
- **🛡️ Güvenli Yapılandırma**: Şifreli ve doğrulanmış konfigürasyon yönetimi
- **🧪 Test Kapsamı**: Kapsamlı birim test desteği

## 📋 Kurulum

### 1. Depoyu Klonlama
```bash
git clone https://github.com/stvowns/balina2.git
cd balina2droid
```

### 2. Sanal Ortam Oluşturma
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 4. Kurulum Script'ini Çalıştırma (Önerilen)
```bash
chmod +x install.sh
./install.sh
```

## ⚙️ Çoklu Cüzdan Yapılandırması

### 1. Telegram Bot Oluşturma
1. Telegram'da [@BotFather](https://t.me/botfather) kullanarak bot oluşturun
2. Bot token'ını kopyalayın

### 2. Chat ID Öğrenme
```bash
python3 get_chat_id.py
```
Bot token'ı girip botunuza mesaj gönderin.

### 3. Çoklu Cüzdan Konfigürasyonu

**Yöntem 1: JSON Konfigürasyonu (Önerilen)**
```bash
# .env dosyasına
WALLETS_JSON={"trading":{"address":"0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45","name":"Trading Wallet","enabled":true},"savings":{"address":"0x1234567890123456789012345678901234567890","name":"Savings Wallet","enabled":true,"telegram_chat_id":"987654321"}}
```

**Yöntem 2: Individual Environment Variables**
```bash
# API anahtarı (zorunlu)
ETHERSCAN_API_KEY=SIZIN_ETHERSCAN_API_KEY

# Global Telegram ayarları
TELEGRAM_BOT_TOKEN=BOT_TOKENINIZ
TELEGRAM_CHAT_ID=GLOBAL_CHAT_ID

# Cüzdan 1
WALLET_1_ADDRESS=0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45
WALLET_1_NAME=Trading Wallet
WALLET_1_ENABLED=true
WALLET_1_TELEGRAM_CHAT_ID=TRADING_CHAT_ID

# Cüzdan 2
WALLET_2_ADDRESS=0x1234567890123456789012345678901234567890
WALLET_2_NAME=Savings Wallet
WALLET_2_ENABLED=true
WALLET_2_EMAIL_RECIPIENT=savings@example.com
```

**Yöntem 3: Tek Cüzdan (Backward Compatibility)**
```bash
WALLET_ADDRESS=0xSINGLE_WALLET_ADDRESS
ETHERSCAN_API_KEY=SIZIN_ETHERSCAN_API_KEY
```

### 4. İsteğe Bağlı Bildirim Ayarları
```bash
# Global Gmail ayarları
EMAIL_SENDER=gmail@gmail.com
EMAIL_PASSWORD=APP_PASSWORD
EMAIL_RECIPIENT=default@example.com

# İleri seviye yapılandırma
CHECK_INTERVAL=600  # 10 dakika
BALANCE_CHANGE_THRESHOLD=0.1  # ETH
POSITION_CHANGE_THRESHOLD=1000  # USD
```

## 🎯 Kullanım

### Cüzdanları Listeleme
```bash
python3 main.py --list
```

### Manuel Kontrol
Tüm cüzdanları bir kez kontrol etmek için:
```bash
python3 main.py --check
```

### Sürekli İzleme
Arkaplanda sürekli izleme başlatmak için:
```bash
python3 main.py
```

### Testleri Çalıştırma
```bash
# Tüm testler
python3 test_runner.py

# Sadece çoklu cüzdan testleri
python3 test_runner.py --multi
```

## 📊 Bildirim Özellikleri

### Cüzdan Bazlı Bildirimler
Her cüzdan için ayrı bildirim kanalları:
- Özel Telegram chat ID
- Özel e-posta alıcıları
- Cüzdan adı bildirimlerde gösterilir

### Bildirim Türleri
- 🚀 **Pozisyon Açıldı**: Yeni pozisyon oluştuğunda
- ✅ **Pozisyon Kapandı**: Pozisyon kapatıldığında
- 🔄 **Pozisyon Değişti**: Anlamlı değişikliklerde
- 📥 **Para Yatırma**: ETH, BTC veya token geldiğinde
- 📤 **Para Çekme**: Cüzdan para gönderdiğinde
- 💰 **Bakiye Değişimi**: Anlamlı ETH değişikliklerinde

### Özet Bildirimleri
- Başlangıç özetleri her cüzdan için
- Genel çoklu cüzdan özeti
- Toplam bakiye raporları

## 🛠️ Yapılandırma Seçenekleri

### Cüzdan Yönetimi
```bash
# Cüzdanları etkinleştirme/devre dışı bırakma
WALLET_1_ENABLED=true
WALLET_2_ENABLED=false

# Cüzdanlara özel isimler
WALLET_1_NAME=Ana Cüzdan
WALLET_2_NAME=Yedekleme Cüzdan
```

### Kontrol ve Eşikler
```bash
# Kontrol sıklığı
CHECK_INTERVAL=300  # 5 dakika

# Bildirim eşikleri
BALANCE_CHANGE_THRESHOLD=0.05  # 0.05 ETH
POSITION_CHANGE_THRESHOLD=500   # $500
```

## 🔧 Test ve Hata Ayıklama

### Telegram Bağlantısı Testi
```bash
python3 test_notification.py
```

### Cüzdan Durumu Kontrolü
```bash
python3 debug_positions.py
```

### Çoklu Cüzdan Testleri
```bash
python3 test_multi_wallet.py
```

## 📁 Temel Dosyalar

- `main.py` - Ana uygulama ve çoklu cüzdan yönetimi
- `multi_wallet_tracker.py` - Çoklu cüzdan izleyici
- `wallet_tracker.py` - Tekil cüzdan takip işlemleri
- `notification_system.py` - Bildirim sistemi
- `config.py` - Konfigürasyon yönetimi
- `test_*.py` - Test dosyaları

## ⚠️ Güvenlik Notları

- **HASSAS BİLGİLER**: API anahtarları ve özel bilgiler asla paylaşmayın
- **KONFİGÜRASYON GÜVENLİĞİ**: Cüzdan adresleri ve formatları doğrulanır
- **API LİMİTLERİ**: Etherscan API kullanım limitlerine dikkat edin
- **ŞİFRELİ SAKLAMA**: Hassas bilgiler için güvenli saklama yöntemleri kullanın

## 📞 Sorun Giderme

### Çoklu Cüzdan Sorunları
1. Cüzdan adreslerinin doğru formatlandığından emin olun
2. Her cüzdan için gerekli izin izinlere sahip olduğunuzdan emin olun
3. Konfigürasyon JSON formatının geçerli olduğunu kontrol edin

### Bildirim Sorunları
1. Her cüzdan için Telegram/Email ayarlarını kontrol edin
2. Global ve cüzdan özel bildirim ayarlarını doğrulayın
3. İnternet bağlantısını ve bot erişimini test edin

### Teknik Destek
```bash
# Log dosyasını kontrol etme
cat transactions.log | tail -20

# Cüzdan durumunu kontrol etme
python3 main.py --check
```