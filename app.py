import streamlit as st
from PIL import Image
import os
import io
from huggingface_hub import InferenceClient

st.set_page_config(page_title="AI Photo Editor Free", page_icon="✨")
st.title("✨ AI Photo Editor")

# Получаем ключ
api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
if not api_key:
    st.error("Ошибка: Ключ HUGGINGFACEHUB_API_TOKEN не найден в Secrets.")
    st.stop()

# Инициализируем клиент Hugging Face
client = InferenceClient(token=api_key)

uploaded_file = st.file_uploader("Выберите фото...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Оригинал', use_column_width=True)
    img_bytes = uploaded_file.getvalue()

    if st.button('Улучшить фото'):
        with st.spinner('Обработка...'):
            try:
                # Используем более простую модель для задач Image-to-Image
                # Многие тяжелые модели требуют времени на "запуск" (loading)
                image = Image.open(io.BytesIO(img_bytes))
                
                # Используем встроенный метод client.image_to_image
                # Это надежнее, чем ручной запрос
                res = client.image_to_image(
                    image=image,
                    model="runwayml/stable-diffusion-v1-5" 
                )
                
                st.image(res, caption='Результат')
            except Exception as e:
                st.error(f"Ошибка при работе с ИИ: {e}")
