import os
import numpy as np
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# 定義類別名稱
class_names = ["apple", "avocado", "banana", "cherry", "kiwi", "mango", "orange", "pineapple", "strawberries", "watermelon"]
secondary_class_names = ["avocado", "banana"]

# 載入模型
model_multiclass = load_model("best_model_1st.keras")  # 第一階段模型（多分類器）
model_binary = load_model("best_model_2nd.keras")  # 第二階段模型（二分類器）

# Streamlit 應用
st.title("水果分類模型")
st.write("上傳一張水果圖片，模型將進行兩階段分類並返回結果！")

uploaded_file = st.file_uploader("選擇一張圖片進行分類", type=["jpg", "png", "jpeg"])

# 圖片預處理
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

if uploaded_file is not None:
    st.image(uploaded_file, caption="上傳的圖片", use_column_width=True)
    
    # 儲存上傳的圖片
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    image = preprocess_image("temp_image.jpg")
    
    try:
        # 第一階段：多分類
        prediction_multiclass = model_multiclass.predict(image)
        predicted_class_index = np.argmax(prediction_multiclass)
        predicted_class = class_names[predicted_class_index]
        confidence_multiclass = np.max(prediction_multiclass)

        # 判斷是否進入第二階段分類
        if predicted_class in ["banana", "avocado"]:
            st.write("### 第一階段分類結果：")
            st.write(f"### 預測類別：{predicted_class} (需進行進一步分類)")
            st.write(f"信心分數：{confidence_multiclass:.2f}")

            # 第二階段：香蕉與酪梨細分
            prediction_binary = model_binary.predict(image)
            binary_class_index = int(prediction_binary[0] >= 0.5)  # 0: avocado, 1: banana
            final_class = secondary_class_names[binary_class_index]
            confidence_binary = prediction_binary[0] if binary_class_index == 1 else 1 - prediction_binary[0]

            st.write("### 第二階段分類結果：")
            st.write(f"### 最終類別：{final_class}")
            st.write(f"信心分數：{confidence_binary:.2f}")
        else:
            st.write("### 第一階段分類結果：")
            st.write(f"### 預測類別：{predicted_class}")
            st.write(f"信心分數：{confidence_multiclass:.2f}")

    except Exception as e:
        st.write(f"分類過程中出現錯誤：{e}")
    finally:
        os.remove("temp_image.jpg")
