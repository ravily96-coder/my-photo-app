import streamlit as st
from PIL import Image
import replicate
import os
import requests
from io import BytesIO

st.set_page_config(page_title="AI Photo Editor Pro", page_icon="✨")
st.title("✨ AI Photo Editor Pro")

# Получение API ключа
try:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
except:
    st.error("Ошибка: REPLICATE_API_TOKEN не найден в Secrets.")
    st.stop()

uploaded_file = st.file_uploader("Выберите фото...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Оригинал', use_column_width=True)
    
    col1, col2, col3 = st.columns(3)

    # Функция обработки
    def process_image(model_path, input_data):
        with st.spinner('Обработка ИИ...'):
            try:
                output_url = replicate.run(model_path, input=input_data)
                response = requests.get(output_url)
                return Image.open(BytesIO(response.content))
            except Exception as e:
                st.error(f"Ошибка: {e}")
                return None

    with col1:
        if st.button('Омолодить'):
            res = process_image("sczhou/codeformer:7ab7596c45b3313814b00b3f986a329639f5474656132119aa5f6c1e08477809", 
                                {"image": uploaded_file, "codeformer_fidelity": 0.5})
            if res: st.image(res, caption='Результат: Омоложение')

    with col2:
        if st.button('Улучшить (Upscale)'):
            res = process_image("nightmareai/real-esrgan:42fed1c4974616d2f7587123985b62b7137f8f9f6007b8a7d23d854408544c9b", 
                                {"image": uploaded_file, "scale": 2})
            if res: st.image(res, caption='Результат: Улучшено')

    with col3:
        if st.button('Убрать шумы'):
            res = process_image("tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3", 
                                {"img": uploaded_file})
            if res: st.image(res, caption='Результат: Без шума')
