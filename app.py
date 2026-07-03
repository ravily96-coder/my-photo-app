import streamlit as st
from PIL import Image
from huggingface_hub import InferenceClient
import io

st.set_page_config(page_title="AI Editor Free", page_icon="✨")
st.title("✨ AI Photo Editor (Free Edition)")

# Получаем токен из секретов
api_key = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
client = InferenceClient(api_key=api_key)

uploaded_file = st.file_uploader("Загрузите портрет...", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Оригинал')
    
    if st.button('Улучшить лицо (GFPGAN)'):
        with st.spinner('Нейросеть работает...'):
            # Конвертируем фото в байты для отправки
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            
            # Вызов модели через Hugging Face
            # Используем популярную модель GFPGAN
            response = client.image_to_image(
                model="ap123/GFPGAN",
                image=img_byte_arr.getvalue()
            )
            
            st.image(response, caption='Результат')
