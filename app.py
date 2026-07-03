import os
import time
from io import BytesIO

import streamlit as st
from PIL import Image, ImageEnhance

# ---------------------------------------------------
# Настройки страницы
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Photo Editor",
    page_icon="✨",
    layout="wide"
)

st.title("✨ AI Photo Editor")
st.write("Загрузите фотографию и улучшите её с помощью искусственного интеллекта.")

# ---------------------------------------------------
# Функция-заглушка AI
# Вместо неё позже подключается Replicate API
# ---------------------------------------------------

def ai_restore(image: Image.Image):

    # Имитация работы нейросети
    time.sleep(3)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.15)

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.1)

    return image


# ---------------------------------------------------
# Загрузка изображения
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Выберите изображение",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Исходное фото")
        st.image(image, use_container_width=True)

    with col2:

        if st.button("🚀 Улучшить фотографию"):

            with st.spinner("AI обрабатывает изображение..."):

                result = ai_restore(image)

            st.subheader("Результат")

            st.image(result, use_container_width=True)

            # -----------------------------
            # Кнопка скачать
            # -----------------------------

            buffer = BytesIO()

            result.save(buffer, format="PNG")

            st.download_button(
                "📥 Скачать",
                data=buffer.getvalue(),
                file_name="ai_result.png",
                mime="image/png"
            )
