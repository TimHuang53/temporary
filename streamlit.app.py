import os
import numpy as np
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# 定義類別名稱
class_names_1 = ["apple", "avocado", "banana", "cherry", "kiwi", "mango", "orange", "pineapple", "strawberries", "watermelon"]
class_names_2 = ["avocado", "banana"]  # 第二個模型只有這兩個類別：酪梨和香蕉

# 載入兩個模型
model_1 = load_model("best_model_1st.keras")  # 第一個模型
model_2 = load_model("best_model_2nd.keras")  # 第二個模型

# Streamlit 應用
st.title("水果分類模型")
st.write("上傳一張水果圖片，模型將會進行分類並返回結果！")

uploaded_file = st.file_uploader("選擇一張圖片進行分類", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="上傳的圖片", use_column_width=True)

    # 圖片預處理函數
    def preprocess_image(image_path):
        img = load_img(image_path, target_size=(224, 224))  # 將圖片調整為 (224, 224)
        img_array = img_to_array(img)  # 將圖片轉換為數組
        img_array = np.expand_dims(img_array, axis=0)  # 增加一個批次維度，形狀為 (1, 224, 224, 3)
        img_array = img_array / 255.0  # 正規化到 [0, 1] 範圍
        return img_array

    # 儲存上傳的圖片
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 預處理圖片
    image = preprocess_image("temp_image.jpg")

    try:
        # 使用第一個模型進行預測
        prediction_1 = model_1.predict(image)
        predicted_class_1 = class_names_1[np.argmax(prediction_1)]  # 找到預測概率最大的類別
        confidence_1 = np.max(prediction_1)  # 取得預測的信心分數

        # 如果預測是香蕉或酪梨，則使用第二個模型進行預測
        if predicted_class_1 in ["banana", "avocado"]:
            prediction_2 = model_2.predict(image)
            predicted_class_2 = class_names_2[np.argmax(prediction_2)]
            confidence_2 = np.max(prediction_2)

            st.write(f"### 預測結果：{predicted_class_2} (信心分數：{confidence_2:.2f})")
        else:
            # 如果第一模型預測不是香蕉或酪梨，則只顯示第一模型的結果
            st.write(f"### 預測結果：{predicted_class_1}")
            st.write(f"### 信心分數：{confidence_1:.2f}")

    except Exception as e:
        # 顯示錯誤訊息
        st.write(f"模型預測過程中出現錯誤：{e}")

    finally:
        # 刪除臨時圖片文件
        os.remove("temp_image.jpg")
