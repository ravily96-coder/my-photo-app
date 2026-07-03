import streamlit as st
from gradio_client import Client
from PIL import Image
import io

st.set_page_config(page_title="AI Photo Editor", page_icon="✨")
st.title("✨ AI Photo Editor Pro")

uploaded_file = st.file_uploader("Загрузите фото:", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Оригинал', use_column_width=True)
    col1, col2, col3 = st.columns(3)

    # Функция для работы с демо-пространствами
    def run_gradio(space_name, api_name, image_path):
        with st.spinner('Нейросеть в работе...'):
            try:
                client = Client(space_name)
                # Вызываем предсказание
                result = client.predict(image=image_path, api_name=api_name)
                return Image.open(result)
            except Exception as e:
                st.error(f"Сервер занят, попробуйте еще раз: {e}")
                return None

    # Кнопка Омолодить (используем стабильное демо GFPGAN)
    with col1:
        if st.button('Омолодить'):
            res = run_gradio("gfpgan/GFPGAN", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Омоложение')

    # Кнопка Убрать фон (используем официальное демо Rembg)
    with col2:
        if st.button('Убрать фон'):
            res = run_gradio("akhaliq/rembg", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Без фона')

    # Кнопка Улучшить (используем стабильное демо Real-ESRGAN)
    with col3:
        if st.button('Улучшить'):
            res = run_gradio("nateraw/real-esrgan", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Улучшено')
