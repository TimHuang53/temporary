import os
import numpy as np
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import ResNet50

# 定義類別名稱
class_names = ["apple", "avocado", "banana", "cherry", "kiwi", "mango", "orange", "pineapple", "strawberries", "watermelon"]

# 載入最佳模型
model = load_model("best_model_mobilenet.keras")

# Streamlit 應用
st.title("水果分類模型")
st.write("上傳一張水果圖片，模型將會進行分類並返回結果！")

uploaded_file = st.file_uploader("選擇一張圖片進行分類", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="上傳的圖片", use_column_width=True)
    
    def preprocess_image(image_path):
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    # 儲存上傳的圖片
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    image = preprocess_image("temp_image.jpg")
    
    try:
        prediction = model.predict(image)
        predicted_class = class_names[np.argmax(prediction)]
        confidence = np.max(prediction)
        st.write(f"### 預測結果：{predicted_class}")
        st.write(f"### 信心分數：{confidence:.2f}")
    except Exception as e:
        st.write(f"模型預測過程中出現錯誤：{e}")
    finally:
        os.remove("temp_image.jpg")
