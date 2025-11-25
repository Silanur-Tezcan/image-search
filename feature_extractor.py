import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
import numpy as np
import os

# --- Modelin Yüklenmesi (Sunucu Başladığında Bir Kez Çalışacak) ---
try:
    # MobileNetV2'yi 'imagenet' ağırlıklarıyla yükle. Son katmanı hariç tut ('include_top=False').
    base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
    FEATURE_EXTRACTOR_MODEL = Model(inputs=base_model.input, outputs=base_model.output)
    print("MobileNetV2 Özellik Çıkarıcı Model Başarıyla Yüklendi.")
except Exception as e:
    print(f"Hata: Model yüklenemedi. İnternet bağlantınızı kontrol edin veya modelin indirildiğinden emin olun. {e}")
    FEATURE_EXTRACTOR_MODEL = None

def extract_features(img_path):
    """
    Belirtilen görüntü yolundan 1280 boyutlu özellik vektörünü çıkarır.
    """
    if FEATURE_EXTRACTOR_MODEL is None:
        return None # Model yüklenemediyse None döndür

    # Görüntüyü yükle ve MobileNetV2'nin beklediği (224, 224) boyuta yeniden boyutlandır.
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    # Tek bir görüntü için 4 boyutlu tensör yap (Batch boyutu için eksen ekle)
    img_array = np.expand_dims(img_array, axis=0) 
    # Görüntüleri modelin beklentisine göre ön işlemden geçir
    processed_img = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # Özellik vektörünü çıkar
    features = FEATURE_EXTRACTOR_MODEL.predict(processed_img)
    
    # Vektörü L2 normuna göre normalize et (Kosinüs benzerliği için)
    normalized_features = features[0] / np.linalg.norm(features[0])
    
    return normalized_features