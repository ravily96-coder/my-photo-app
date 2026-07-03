import streamlit as st
from PIL import Image
import replicate
import os
import requests
from io import BytesIO

# --- Конфигурация ---
st.set_page_config(page_title="AI Rejuvenator Pro", page_icon="✨")
st.title("✨ AI Photo Rejuvenator Pro")
st.write("Загрузите портрет, чтобы нейросеть убрала возраст и улучшила детализацию.")

# Получаем API ключ из секретов Streamlit (безопасно)
try:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
except KeyError:
    st.error("Ошибка: REPLICATE_API_TOKEN не найден в настройках Secrets.")
    st.stop() # Останавливаем выполнение, если ключа нет

# --- Интерфейс ---
uploaded_file = st.file_uploader("Выберите портрет (файл)...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Отображаем оригинал
    image = Image.open(uploaded_file)
    st.image(image, caption='Оригинал', use_column_width=True)
    
    if st.button('Омолодить фото с AI'):
        with st.spinner('Работает нейросеть CodeFormer... Это займет 5-15 секунд.'):
            try:
                # --- Магия ИИ (Универсальный вызов) ---
                # Используем прямой вызов модели без поиска версии вручную
                input_data = {
                    "image": uploaded_file,
                    "codeformer_fidelity": 0.5,
                    "background_enhance": True,
                    "face_upsample": True,
                    "upscale": 2
                }
                
                # Запускаем модель напрямую
                output = replicate.run(
                    "sczhou/codeformer:7ab7596c45b3313814b00b3f986a329639f5474656132119aa5f6c1e08477809",
                    input=input_data
                )
                
                # output в новых версиях обычно сразу возвращает URL или объект
                output_url = output 
                
                # --- Скачивание результата ---
                response = requests.get(output_url)
                result_image = Image.open(BytesIO(response.content))
                
                # Запускаем модель
                output_url = version.predict(
                    image=uploaded_file,
                    codeformer_fidelity=0.5, # От 0 (лучшее качество лица) до 1 (лучшее сходство)
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2 # Увеличить в 2 раза
                )
                
                # --- Скачивание результата ---
                response = requests.get(output_url)
                result_image = Image.open(BytesIO(response.content))
                
                # --- Отображение ---
                st.success("Готово!")
                st.image(result_image, caption='Результат (AI омоложение)', use_column_width=True)
                
                # Кнопка для скачивания
                buf = BytesIO()
                result_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(
                    label="Скачать результат",
                    data=byte_im,
                    file_name="rejuvenated_photo.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error(f"Произошла ошибка: {e}")

# --- Футер ---
st.write("---")
st.write("Технология: CodeFormer (via Replicate API).")
