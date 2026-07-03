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
            response = # Используем универсальный метод, который сам находит модель для улучшения изображений
            # GFPGAN в облаке часто недоступен через API напрямую, поэтому используем другой подход
            try:
                # Отправляем запрос на задачу image-to-image
                # Мы используем модель, которая часто доступна в бесплатном Inference API
                model_id = "runwayml/stable-diffusion-v1-5" 
                
                # Примечание: API Hugging Face меняется, поэтому мы используем более простой POST запрос
                import requests
                API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
                headers = {"Authorization": f"Bearer {api_key}"}
                
                response = requests.post(API_URL, headers=headers, data=img_byte_arr.getvalue())
                result_image = Image.open(io.BytesIO(response.content))
                st.image(result_image, caption='Результат')
                
            except Exception as e:
                st.error(f"Не удалось обработать изображение: {e}")
            
            st.image(response, caption='Результат')
