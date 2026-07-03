import streamlit as st
from huggingface_hub import InferenceClient
import io
from PIL import Image

st.set_page_config(page_title="AI Photo Editor", page_icon="✨")
st.title("✨ AI Photo Editor")

# Используем InferenceClient — это самый надежный метод от самих создателей Hugging Face
# Ключ не нужен для многих публичных моделей
client = InferenceClient()

uploaded_file = st.file_uploader("Загрузите фото:", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Оригинал', use_column_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Функция обработки
    def process_image(model_id, image_bytes):
        with st.spinner('Обработка...'):
            try:
                # Отправляем картинку напрямую в модель
                image = client.image_to_image(model=model_id, image=image_bytes)
                return image
            except Exception as e:
                st.error(f"Ошибка модели: {e}")
                return None

    img_bytes = uploaded_file.getvalue()

    with col1:
        if st.button('Омолодить'):
            # Используем стабильную модель для восстановления лиц
            res = process_image("sczhou/CodeFormer", img_bytes)
            if res: st.image(res, caption='Результат: Омоложение')

    with col2:
        if st.button('Убрать фон'):
            res = process_image("briaai/RMBG-1.4", img_bytes)
            if res: st.image(res, caption='Результат: Без фона')

    with col3:
        if st.button('Улучшить'):
            res = process_image("stabilityai/stable-diffusion-x4-upscaler", img_bytes)
            if res: st.image(res, caption='Результат: Улучшено')
