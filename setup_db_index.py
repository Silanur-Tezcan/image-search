import os
import faiss
import pickle
import numpy as np
import sqlite3
from feature_extractor import extract_features # Kendi yazdığımız dosya

# --- Ayarlar ---
IMAGE_DIR = 'product_images'
DATABASE_NAME = 'products.db'
INDEX_DIR = 'index'
INDEX_FILE = os.path.join(INDEX_DIR, 'faiss.index')
ID_MAP_FILE = os.path.join(INDEX_DIR, 'product_ids.pkl')
FEATURE_DIMENSION = 1280 # MobileNetV2'nin çıktı boyutu

def init_db():
    """SQLite veritabanını oluşturur ve örnek verileri ekler."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS products')
    c.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            file_name TEXT,
            name TEXT,
            category TEXT,
            price REAL,
            stock_count INTEGER
        )
    ''')
    
    # Örnek Veri Ekleme (product_images klasöründeki her dosya için bir satır oluşturulur)
    print("Veritabanına örnek ürün bilgileri ekleniyor...")
    image_paths = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))])
    
    for i, file_name in enumerate(image_paths):
        # Basit bir örnek veri oluşturma
        product_id = i + 1
        product_name = f"Stok Ürünü #{product_id}"
        category = "Giyim" if i % 3 == 0 else "Elektronik" if i % 3 == 1 else "Ev Aletleri"
        price = 100.0 + (i * 15.5)
        stock_count = 50 - (i % 20)
        
        c.execute('INSERT INTO products (id, file_name, name, category, price, stock_count) VALUES (?, ?, ?, ?, ?, ?)',
                  (product_id, file_name, product_name, category, price, stock_count))
                  
    conn.commit()
    conn.close()
    print("SQLite Veritabanı Başarıyla Oluşturuldu.")


def create_faiss_index():
    """Tüm ürün görsellerinin özelliklerini çıkarır ve Faiss indeksi oluşturur."""
    print("Faiss İndeksi oluşturuluyor...")
    
    # Tüm görselleri bul
    image_paths = sorted([os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))])
    
    all_features = []
    product_ids = []

    if not image_paths:
        print("Hata: product_images klasöründe hiç görsel bulunamadı.")
        return

    # Görsellerden özellikleri çıkar
    for i, path in enumerate(image_paths):
        print(f"Özellik çıkarılıyor: {i+1}/{len(image_paths)} - {os.path.basename(path)}")
        features = extract_features(path)
        if features is not None:
            all_features.append(features)
            # Veritabanındaki ID'ler 1'den başlar (i+1)
            product_ids.append(i + 1) 
    
    if not all_features:
        print("Hata: Hiçbir görüntüden özellik çıkarılamadı.")
        return

    all_features_np = np.array(all_features).astype('float32')

    # Faiss İndeksi Oluştur
    # IndexFlatL2: En basit ve en doğru (Brute-Force) arama metodu.
    index = faiss.IndexFlatL2(FEATURE_DIMENSION) 
    index.add(all_features_np) 

    # İndeks ve ID Map'i kaydet
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    with open(ID_MAP_FILE, 'wb') as f:
        pickle.dump(product_ids, f)

    print(f"\nFaiss İndeksi ({index.ntotal} ürün) başarıyla oluşturuldu ve {INDEX_FILE} dosyasına kaydedildi.")
    print(f"Ürün ID map dosyası {ID_MAP_FILE} konumuna kaydedildi.")


if __name__ == '__main__':
    # 1. product_images klasörünü kontrol et
    os.makedirs(IMAGE_DIR, exist_ok=True)
    if not os.listdir(IMAGE_DIR):
        print(f"Lütfen '{IMAGE_DIR}' klasörüne en az birkaç ürün görseli ekleyin ve tekrar çalıştırın.")
    else:
        # 2. Veritabanını hazırla
        init_db()
        # 3. Faiss İndeksini oluştur
        create_faiss_index()