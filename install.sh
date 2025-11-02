#!/bin/bash
# Kripto Cüzdan Takip Yazılımı Kurulum Scripti

echo "🚀 Kripto Cüzdan Takip Yazılımı Kuruluyor..."

# Python'ın yüklü olup olmadığını kontrol et
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı. Lütfen önce Python3 kurun."
    exit 1
fi

# Python versiyonunu kontrol et
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
echo "✅ Python3 $python_version bulundu"

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python3 -m venv venv
else
    echo "✅ Sanal ortam zaten mevcut"
fi

# Sanal ortamı aktifleştirme
echo "🔄 Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# .env dosyasını oluşturma
if [ ! -f ".env" ]; then
    echo "📝 .env dosyası oluşturuluyor..."
    cp .env.example .env
    echo "✅ .env dosyası oluşturuldu."
else
    echo "✅ .env dosyası zaten mevcut"
fi

# Gerekli kütüphaneleri yükleme
echo "📚 Kütüphaneler yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Kurulum tamamlandı!"
echo ""
echo "🎉 Kurulum tamamlandı! Başlatmak için:"
echo "1. nano .env    # .env dosyasını düzenleyin"
echo "2. python main.py    # Uygulamayı başlatın"
