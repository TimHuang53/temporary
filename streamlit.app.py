import numpy as np
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from io import BytesIO

# 定義類別名稱
class_names = [
    "apple", "avocado", "banana", "cherry", "kiwi",
    "mango", "orange", "pineapple", "strawberries", "watermelon"
]

# 載入模型
MODEL_PATH = "best_model_mobilenet.keras"
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    st.error(f"無法載入模型。請檢查模型檔案是否存在並且格式正確。詳細錯誤：{e}")
    st.stop()

# Streamlit 應用
st.title("水果分類模型")
st.write("上傳一張水果圖片，模型將會進行分類並返回結果！")

# 上傳圖片
uploaded_file = st.file_uploader("選擇一張圖片進行分類", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 顯示上傳的圖片
    st.image(uploaded_file, caption="上傳的圖片", use_column_width=True)
    
    def preprocess_image(file):
        """處理上傳的圖片以適配模型"""
        img = load_img(BytesIO(file.getbuffer()), target_size=(224, 224))  # 調整圖片大小
        img_array = img_to_array(img) / 255.0  # 歸一化處理
        img_array = np.expand_dims(img_array, axis=0)  # 增加批次維度
        return img_array

    try:
        # 處理圖片
        image = preprocess_image(uploaded_file)
        # 模型預測
        prediction = model.predict(image)
        predicted_class = class_names[np.argmax(prediction)]
        confidence = np.max(prediction)

        # 顯示結果
        st.write(f"### 預測結果：{predicted_class}")
        st.write(f"### 信心分數：{confidence:.2f}")
    except Exception as e:
        st.error(f"模型預測過程中出現錯誤：{e}")
