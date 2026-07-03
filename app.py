import streamlit as st
from gradio_client import Client
from PIL import Image
import io

st.set_page_config(page_title="AI Photo Editor Pro", page_icon="✨")
st.title("✨ AI Photo Editor Pro")

uploaded_file = st.file_uploader("Выберите фото...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Оригинал', use_column_width=True)
    
    col1, col2, col3 = st.columns(3)

    # Функция обработки через Gradio
    def process_ai(client_path, api_name, file_input):
        with st.spinner('ИИ думает...'):
            try:
                client = Client(client_path)
                result = client.predict(image=file_input, api_name=api_name)
                # Gradio возвращает путь к файлу или объект, открываем его
                return Image.open(result)
            except Exception as e:
                st.error(f"Ошибка при обработке: {e}")
                return None

    # Кнопка 1: Улучшение лиц (GFPGAN)
    with col1:
        if st.button('Улучшить лицо'):
            res = process_ai("gfpgan/GFPGAN", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Лицо')

    # Кнопка 2: Апскейл (Real-ESRGAN)
    with col2:
        if st.button('Увеличить (4x)'):
            res = process_ai("nateraw/real-esrgan", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Увеличено')

    # Кнопка 3: Удаление фона (Rembg)
    with col3:
        if st.button('Убрать фон'):
            res = process_ai("akhaliq/rembg", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Без фона')
