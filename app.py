import streamlit as st
from PIL import Image
import os
import requests
import io

st.set_page_config(page_title="AI Photo Editor Free", page_icon="✨")
st.title("✨ AI Photo Editor Pro")

# Получаем ключ
api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
if not api_key:
    st.error("Ошибка: Ключ HUGGINGFACEHUB_API_TOKEN не найден в Secrets.")
    st.stop()

uploaded_file = st.file_uploader("Выберите фото...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Оригинал', use_column_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Функция для отправки запроса
    def call_ai_model(model_id, image_bytes):
        API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(API_URL, headers=headers, data=image_bytes)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            st.error(f"Ошибка API ({model_id}): {response.status_code}")
            return None

    img_bytes = uploaded_file.getvalue()

    with col1:
        if st.button('Улучшить (Upscale)'):
            with st.spinner('Апскейлинг...'):
                res = call_ai_model("stabilityai/stable-diffusion-x4-upscaler", img_bytes)
                if res: st.image(res, caption='Результат: Улучшено')

    with col2:
        if st.button('Цветокоррекция'):
            with st.spinner('Обработка...'):
                # Используем модель для стилизации/улучшения цвета
                res = call_ai_model("sayakpaul/sd-model-finetuned-lora-t2i", img_bytes)
                if res: st.image(res, caption='Результат: Цвета')

    with col3:
        if st.button('Очистка'):
            with st.spinner('Очистка...'):
                # Модель для шумоподавления
                res = call_ai_model("shadowlilac/sd-model-denoise", img_bytes)
                if res: st.image(res, caption='Результат: Чистое фото')
