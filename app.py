import streamlit as st
from gradio_client import Client
from PIL import Image
import io

st.set_page_config(page_title="AI Photo Master", page_icon="✨")
st.title("✨ AI Photo Editor Pro")

uploaded_file = st.file_uploader("Загрузите фото для обработки...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Оригинал', use_column_width=True)
    
    col1, col2, col3 = st.columns(3)

    # Универсальная функция для запуска
    def run_tool(space_id, image):
        with st.spinner('Подключаюсь к ИИ...'):
            try:
                client = Client(space_id)
                # Выводим список доступных функций, если не знаем имя
                # Мы берем первую доступную функцию из списка
                api_name = client.view_api(print_json=False, return_format="dict")['named_endpoints'][0]
                
                result = client.predict(image=image, api_name=api_name)
                return Image.open(result)
            except Exception as e:
                st.error(f"Ошибка: {e}")
                return None

    with col1:
        if st.button('Омолодить'):
            # CodeFormer для реставрации лиц
            res = run_tool("sczhou/CodeFormer", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Омоложение')

    with col2:
        if st.button('Убрать фон'):
            # Rembg для удаления фона
            res = run_tool("abhishek/rembg", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Без фона')

    with col3:
        if st.button('Улучшить (Upscale)'):
            # Real-ESRGAN для улучшения качества и детализации
            res = run_tool("nateraw/real-esrgan", "/predict", uploaded_file)
            if res: st.image(res, caption='Результат: Улучшено')
