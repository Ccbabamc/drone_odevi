# Drone Filo Optimizasyonu Projesi Planı

## Proje Özeti
Bu proje, enerji limitleri ve uçuş yasağı bölgeleri gibi dinamik kısıtlar altında çalışan drone'lar için en uygun teslimat rotalarının belirlenmesini sağlayan bir algoritma geliştirmeyi amaçlamaktadır.

## Teknik Mimari

### Ana Modüller
1. **main.py**
   - Programın giriş noktası
   - Modüller arası koordinasyon
   - Kullanıcı arayüzü yönetimi

2. **config.py**
   - Yapılandırma ayarları
   - Sistem parametreleri
   - Sabit değerler

3. **data_generator.py**
   - Rastgele drone verileri üretimi
   - Teslimat noktaları oluşturma
   - Uçuş yasağı bölgeleri tanımlama

4. **optimizer.py**
   - Optimizasyon algoritmaları yönetimi
   - Rota planlaması
   - Kısıt kontrolleri

5. **visualizer.py**
   - Harita görselleştirme
   - Performans grafikleri
   - İstatistik raporları

### Veri Yapıları (models.py)
1. **Drone Sınıfı**
   - ID
   - Maksimum ağırlık
   - Batarya kapasitesi
   - Hız
   - Başlangıç pozisyonu

2. **Teslimat Noktası Sınıfı**
   - ID
   - Pozisyon
   - Paket ağırlığı
   - Öncelik seviyesi
   - Zaman penceresi

3. **Uçuş Yasağı Bölgesi Sınıfı**
   - ID
   - Koordinatlar
   - Aktif zaman aralığı

### Algoritmalar
1. **a_star.py**
   - A* algoritması implementasyonu
   - Rota optimizasyonu
   - Engel kaçınma mantığı

2. **genetic_algorithm.py**
   - Popülasyon yönetimi
   - Çaprazlama operatörleri
   - Mutasyon işlemleri
   - Uygunluk fonksiyonu

3. **constraint_solver.py**
   - Kısıt programlama çözücüsü
   - Dinamik kısıt yönetimi
   - Çözüm optimizasyonu

### Yardımcı Modüller (utils.py)
- Graf işlemleri (NetworkX entegrasyonu)
- Zaman hesaplamaları
- Mesafe hesaplamaları

### Görselleştirme
1. **Harita Görünümü**
   - Folium ile etkileşimli harita
   - Drone rotaları
   - Yasak bölgeler

2. **İstatistik Görünümü**
   - Performans grafikleri
   - Teslimat istatistikleri
   - Optimizasyon metrikleri

## Teknoloji Yığını
```python
# Temel Kütüphaneler
numpy==1.24.3
networkx==3.1
scipy==1.10.1

# Görselleştirme
folium==0.14.0
matplotlib==3.7.1

# Test ve Geliştirme
pytest==7.3.1
black==23.3.0
```

## Geliştirme Aşamaları

### 1. Temel Altyapı (1. Hafta)
- [ ] Veri yapılarının implementasyonu
- [ ] Veri üreteci geliştirme
- [ ] Birim testlerin yazılması

### 2. Algoritma Geliştirme (2. Hafta)
- [ ] A* algoritması implementasyonu
- [ ] Genetik algoritma implementasyonu
- [ ] CSP çözücü implementasyonu

### 3. Optimizasyon ve Test (3. Hafta)
- [ ] Performans optimizasyonu
- [ ] Test senaryolarının çalıştırılması
- [ ] Hata ayıklama ve iyileştirme

### 4. Görselleştirme ve Dokümantasyon (4. Hafta)
- [ ] Harita arayüzü geliştirme
- [ ] İstatistik göstergeleri ekleme
- [ ] Dokümantasyon ve README hazırlama

## Test Senaryoları
1. **Senaryo 1**
   - 5 drone
   - 20 teslimat
   - 2 uçuş yasağı bölgesi

2. **Senaryo 2**
   - 10 drone
   - 50 teslimat
   - 5 dinamik uçuş yasağı bölgesi

## Performans Metrikleri
- Tamamlanan teslimat yüzdesi
- Ortalama enerji tüketimi
- Algoritma çalışma süresi
- 50+ teslimat noktası için < 1 dakika hedefi