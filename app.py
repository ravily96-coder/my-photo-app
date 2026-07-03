import streamlit as st
from gradio_client import Client
from PIL import Image
import io

st.set_page_config(page_title="AI Photo Pro", page_icon="✨")
st.title("✨ AI Photo Editor Pro")

uploaded_file = st.file_uploader("Выберите фото...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Оригинал', use_column_width=True)
    
    col1, col2, col3 = st.columns(3)

    def run_inference(space_id, api_name, image):
        with st.spinner('ИИ обрабатывает...'):
            try:
                client = Client(space_id)
                # Передаем файл как путь или объект
                result = client.predict(image=image, api_name=api_name)
                return Image.open(result)
            except Exception as e:
                st.error(f"Модель временно недоступна: {e}")
                return None

    with col1:
        if st.button('Улучшить лицо'):
            res = run_inference("radames/face-restoration", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Лицо')

    with col2:
        if st.button('Убрать фон'):
            res = run_inference("abhishek/rembg", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Без фона')

    with col3:
        if st.button('Увеличить (Upscale)'):
            # Модель для апскейлинга
            res = run_inference("nateraw/real-esrgan", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Увеличен')
