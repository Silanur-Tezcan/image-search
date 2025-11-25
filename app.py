import os
import faiss
import pickle
import numpy as np
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from feature_extractor import extract_features 

# --- Ayarlar ---
# UPLOAD_FOLDER'ı statik dosyaların içinde olacak şekilde güncelliyoruz ki tarayıcı erişebilsin.
UPLOAD_FOLDER = 'static/uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
INDEX_FILE = 'index/faiss.index'
ID_MAP_FILE = 'index/product_ids.pkl'
DATABASE_NAME = 'products.db'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Global Kaynak Yükleme ---
FAISS_INDEX = None
PRODUCT_IDS = []

def load_resources():
    """Sunucu başladığında Faiss indeksi ve ID map'i yükler."""
    global FAISS_INDEX, PRODUCT_IDS
    
    print("\n--- Kaynaklar Yükleniyor ---")
    
    try:
        # 1. Faiss İndeksini Yükle
        FAISS_INDEX = faiss.read_index(INDEX_FILE)
        print(f"Faiss İndeksi ({FAISS_INDEX.ntotal} ürün) yüklendi.")
    except Exception as e:
        print(f"HATA: Faiss indeksi yüklenemedi. setup_db_index.py'yi çalıştırdınız mı? Hata: {e}")
        
    try:
        # 2. ID Map'i Yükle
        with open(ID_MAP_FILE, 'rb') as f:
            PRODUCT_IDS = pickle.load(f)
        print(f"{len(PRODUCT_IDS)} Ürün ID'si Yüklendi.")
    except Exception as e:
        print(f"HATA: ID map dosyası yüklenemedi. Hata: {e}")

load_resources() 

# --- Veritabanı Yardımcı Fonksiyonu ---
def get_product_data_from_db(product_id):
    """Verilen ID'ye karşılık gelen ürün bilgilerini SQLite'tan çeker."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = c.fetchone()
    conn.close()
    
    return dict(row) if row else None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rota Tanımları ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            return redirect(request.url)
            
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Yüklenen dosyayı kaydet
            file.save(filepath)
            
            return redirect(url_for('search', query_path=filepath))

    return render_template('index.html')

# app.py'de /search rotası (DÜZELTİLMİŞ KOD)

@app.route('/search')
def search():
    query_path = request.args.get('query_path')
    
    # query_path'i static/uploads yolu olarak yeniden inşa ediyoruz
    full_query_path = os.path.join(os.getcwd(), query_path) 

    if not os.path.exists(full_query_path) or FAISS_INDEX is None:
        return redirect(url_for('index'))

    k = 20 # Daha fazla sonuç isteyelim ve sonra filtreleyelim.
    results = []
    found_ids = set() # YENİ: Tekrarlayan ID'leri engellemek için set kullanıyoruz.
    
    try:
        # 1. Özellik Çıkarma
        query_vector = extract_features(full_query_path).astype('float32')
        if query_vector is None:
            raise Exception("Özellik çıkarma başarısız oldu.")
            
        query_vector = np.expand_dims(query_vector, axis=0) 
        faiss.normalize_L2(query_vector)

        # 2. Faiss Arama (D: Uzaklıklar, I: İndeksler)
        D, I = FAISS_INDEX.search(query_vector, k) 
        
        # 3. Sonuçları İşle ve Veritabanından Bilgileri Çek (Filtreleme Burada Yapılır)
        for i, distance in zip(I[0], D[0]):
            product_db_id = PRODUCT_IDS[i]
            
            # --- FİLTRE 1: ID Tekrarını Engelle ---
            if product_db_id in found_ids:
                continue 
                
            # Benzerlik Skoru Hesaplama (Hassasiyet düzeltilmiş hali)
            clipped_distance = np.clip(distance, 0.0, 2.0) 
            similarity_score = 1 - (clipped_distance / 2)
            
            # --- FİLTRE 2: Anlamsız Sonuçları Engelle ---
            # Benzerlik %5'in altındaysa veya 0.00 ise, bu sonucu atlayalım.
            if similarity_score < 0.05: 
                # Eğer ilk sonuç dışında skor çok düşükse, bu muhtemelen alakasızdır.
                # Eğer kola görseline benzeyen yoksa bu filtre ile sonuç bulunamadı deriz.
                continue 
            
            product_data = get_product_data_from_db(product_db_id) 
            
            if product_data:
                # Sonuç yapısına benzerlik skorunu ekle
                product_data['similarity'] = f"{similarity_score * 100:.2f}%"
                
                results.append(product_data)
                found_ids.add(product_db_id) # Yeni bulunan ID'yi listeye ekle

        # Eğer sonuç yoksa, sonuç bulunamadı diyeceğiz
        if not results:
             # Burada k=20'den gelen sonuçların hepsi filtrelenmiştir.
             pass # Veya kullanıcıya özel bir mesaj verebilirsiniz.
            
    except Exception as e:
        print(f"Arama sırasında kritik hata oluştu: {e}")
        
    # query_image için sadece dosya adını kullan
    query_image_name = os.path.basename(query_path) 
    
    # NOTE: results.html dosyasını, 'results' boşsa "Görüntü bulunamadı" diyecek şekilde ayarladık.
    return render_template('results.html', results=results, query_image=query_image_name)
if __name__ == '__main__':
    # Gerekli klasörleri oluştur
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('index', exist_ok=True)
    os.makedirs('static/product_images', exist_ok=True)
    
    # Flask uygulamasını başlat
    app.run(debug=True)