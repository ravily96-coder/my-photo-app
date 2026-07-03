import streamlit as st
from PIL import Image
import os
import requests
import io

st.set_page_config(page_title="AI Photo Editor Free", page_icon="✨")
st.title("✨ AI Photo Editor")

# Получаем ключ из переменных окружения
api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
if not api_key:
    st.error("Ошибка: Ключ HUGGINGFACEHUB_API_TOKEN не найден в настройках Secrets.")
    st.stop()

uploaded_file = st.file_uploader("Выберите фото...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Оригинал', use_column_width=True)
    
    if st.button('Улучшить фото'):
        with st.spinner('Обработка через Hugging Face...'):
            try:
                # Адрес модели для апскейлинга (улучшения качества)
                API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-x4-upscaler"
                headers = {"Authorization": f"Bearer {api_key}"}
                
                # Подготовка данных
                img_bytes = uploaded_file.getvalue()
                
                # Запрос к API
                response = requests.post(API_URL, headers=headers, data=img_bytes)
                
                if response.status_code == 200:
                    result_image = Image.open(io.BytesIO(response.content))
                    st.image(result_image, caption='Результат (Улучшено)')
                else:
                    st.error(f"Ошибка API: {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.error(f"Не удалось обработать: {e}")
            
           
