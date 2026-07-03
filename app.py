import streamlit as st
from gradio_client import Client, handle_file
import os
import uuid
import tempfile
from PIL import Image

# Заголовок страницы
st.set_page_config(page_title="AI Face Restore", page_icon="✨")
st.title("✨ AI Face Restoration (CodeFormer)")

# 7. Client создаётся один раз и кешируется
@st.cache_resource
def get_client():
    try:
        # 6. Проверка подключения
        client = Client("sczhou/CodeFormer")
        return client
    except Exception as e:
        st.error(f"❌ Не удалось подключиться к серверу HuggingFace: {e}")
        return None

client = get_client()

uploaded_file = st.file_uploader("Выберите фото для улучшения (JPG, PNG):", type=["jpg", "png", "jpeg"])

if uploaded_file and client:
    # 5. Проверка размера файла (ограничим 5MB)
    MAX_FILE_SIZE_MB = 5
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.warning(f"⚠️ Файл слишком большой. Максимальный размер: {MAX_FILE_SIZE_MB} MB.")
        st.stop()

    # Отображение оригинала
    try:
        image_pil = Image.open(uploaded_file)
        # 8. use_container_width вместо устаревшего use_column_width
        st.image(image_pil, caption='Оригинал', use_container_width=True)
    except Exception as e:
        st.error(f"❌ Ошибка чтения файла: {e}")
        st.stop()

    # Настройки
    fidelity = st.slider("CodeFormer Fidelity (0 - качество, 1 - сходство):", 0.0, 1.0, 0.7)
    background_enhance = st.checkbox("Улучшение фона", value=True)
    face_upsample = st.checkbox("Увеличение разрешения лица", value=True)

    if st.button('🚀 Улучшить лицо'):
        # 10. Используем NamedTemporaryFile для автоматической очистки и изоляции пользователей
        # 4. Уникальное имя файла
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_input:
            image_pil.save(tmp_input.name)
            tmp_input_path = tmp_input.name

        # 11. Индикатор прогресса
        progress_text = "Идет обработка, пожалуйста, подождите..."
        with st.spinner(progress_text):
            try:
                # 1. Правильный вызов API (согласно актуальной версии CodeFormer)
                # Мы используем handle_file(), чтобы Gradio корректно отправил файл
                result = client.predict(
                    image=handle_file(tmp_input_path),
                    background_enhance=background_enhance,
                    face_upsample=face_upsample,
                    codeformer_fidelity=fidelity,
                    api_name="/predict"
                )
                
                # 2. Корректная обработка результата
                # result может быть строкой (путь) или кортежем. Нам нужен путь.
                output_path = result if isinstance(result, str) else result[0]
                
                if output_path and os.path.exists(output_path):
                    st.success("✅ Готово!")
                    st.image(output_path, caption='Результат', use_container_width=True)
                    
                    # 9. Возможность скачать результат
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Скачать результат",
                            data=f,
                            file_name="codeformer_result.png",
                            mime="image/png"
                        )
                else:
                    st.error("❌ API вернуло некорректный путь к файлу.")
                    # Для отладки можно показать: st.write(result)

            except Exception as e:
                st.error(f"❌ Ошибка при вызове API CodeFormer: {e}")
            finally:
                # 10. Очистка временного файла
                if os.path.exists(tmp_input_path):
                    os.remove(tmp_input_path)

elif not client:
    st.info("🔄 Инициализация клиента нейросети...")
else:
    st.info("📥 Пожалуйста, загрузите фотографию.")

# Дополнительный совет: если ошибка 403/422, используйте client.view_api()
# для проверки актуальных параметров.
