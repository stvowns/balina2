# Balina2Droid Proje Genel Bakış

## Proje Amacı
Balina2Droid, çoklu Ethereum cüzdanlarını ve Hyperliquid pozisyonlarını izleyen, Telegram bildirimleriyle anında değişimleri raporlayan bir kripto cüzdan takip sistemidir.

## Teknoloji Stack'i
- **Python 3.7+**: Ana programlama dili
- **requests>=2.25.1**: HTTP API çağrıları için
- **schedule>=1.1.0**: Zamanlayıcı görevleri için
- **web3>=5.28.0**: Ethereum blockchain etkileşimi için
- **python-telegram-bot>=13.7**: Telegram bot entegrasyonu
- **python-dotenv>=0.19.0**: Environment variable yönetimi

## Ana Özellikler
- Çoklu cüzdan desteği (sınırsız)
- Gerçek zamanlı bildirimler (Telegram, Email, Console)
- Bakiye değişikliği takibi
- Hyperliquid pozisyon takibi
- Transfer ve deposit/withdrawal bildirimleri
- Pozisyon vurgulama (değişen varlığı işaretleme)

## Proje Yapısı
```
balina2droid/
├── main.py                    # Ana uygulama giriş noktası
├── config.py                  # Konfigürasyon yönetimi
├── notification_system.py     # Bildirim sistemi
├── wallet_tracker.py          # Tekil cüzdan takibi
├── multi_wallet_tracker.py    # Çoklu cüzdan yönetimi
├── utils.py                   # Yardımcı fonksiyonlar
├── logger_config.py           # Log yapılandırması
├── telegram_utilities.py      # Telegram yardımcıları
├── test_*.py                  # Test dosyaları
├── requirements.txt           # Python bağımlılıkları
└── .env                       # Environment variables
```

## Kod Stili ve Konvansiyonları
- Python PEP 8 standartlarına uyuluyor
- Type hints kullanımı (typing modülü)
- Docstring'ler mevcut ama tutarsız
- Error handling mevcut ama zayıf
- Sınıf tabanlı mimari
- Global değişkenlerden kaçınılıyor

## Test Komutları
```bash
python3 test_runner.py        # Tüm testleri çalıştır
python3 main.py --check       # Manuel kontrol
python3 main.py --list        # Cüzdanları listele
```

## Geliştirme Komutları
```bash
source venv/bin/activate      # Virtual environment aktifleştirme
pip install -r requirements.txt  # Bağımlılıkları kurma
python3 main.py               # Uygulamayı başlatma
```

## Güvenlik Özellikleri
- Ethereum adres validasyonu
- Environment variable şifreleme
- API anahtarı koruması
- SMTP authentication

## Kalıp ve Tasarım Kararları
- Singleton pattern kullanımı (notification systems)
- Factory pattern (tracker creation)
- Observer pattern (notification delivery)
- Configuration validation pattern
- Error handling pattern