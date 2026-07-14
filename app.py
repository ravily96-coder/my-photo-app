from ai_models import ai
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import time

# -------------------------------------------------
# НАСТРОЙКА СТРАНИЦЫ
# -------------------------------------------------

st.set_page_config(
    page_title="AI Photo Editor Pro",
    page_icon="✨",
    layout="wide"
)

# -------------------------------------------------
# CSS
# -------------------------------------------------

st.markdown("""
<style>

.main{
    background:#f4f6fb;
}

h1{
    color:#2E86DE;
}

.stButton>button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# ЗАГОЛОВОК
# -------------------------------------------------

st.title("✨ AI Photo Editor PRO")

st.write(
    "Профессиональный AI редактор фотографий."
)

# -------------------------------------------------
# БОКОВОЕ МЕНЮ
# -------------------------------------------------

st.sidebar.title("🧠 AI Инструменты")

mode = st.sidebar.radio(

    "Выберите режим",

    [

        "🚀 Улучшение фото",

        "👶 Омоложение",

        "🖼 Восстановление",

        "🎨 Улучшение цветов",

        "✨ Повышение резкости",

        "📸 Удаление шума"

    ]

)

strength = st.sidebar.slider(

    "Сила эффекта",

    1,

    10,

    5

)

# -------------------------------------------------
# AI ФУНКЦИИ
# -------------------------------------------------

def enhance_photo(img):

    time.sleep(2)

    img = ImageEnhance.Sharpness(img).enhance(
        1 + strength / 5
    )

    img = ImageEnhance.Contrast(img).enhance(
        1 + strength / 20
    )

    img = ImageEnhance.Color(img).enhance(
        1 + strength / 30
    )

    return img


def rejuvenate(img):

    time.sleep(2)

    img = img.filter(ImageFilter.SMOOTH_MORE)

    img = img.filter(
        ImageFilter.GaussianBlur(
            radius=strength / 8
        )
    )

    img = ImageEnhance.Color(img).enhance(1.15)

    img = ImageEnhance.Brightness(img).enhance(1.05)

    img = ImageEnhance.Contrast(img).enhance(1.05)

    return img


def restore(img):

    time.sleep(2)

    img = ImageEnhance.Sharpness(img).enhance(2)

    img = ImageEnhance.Contrast(img).enhance(1.2)

    img = ImageEnhance.Color(img).enhance(1.2)

    return img


def colors(img):

    time.sleep(2)

    img = ImageEnhance.Color(img).enhance(
        1 + strength / 10
    )

    img = ImageEnhance.Contrast(img).enhance(1.1)

    return img


def sharpen(img):

    time.sleep(2)

    img = ImageEnhance.Sharpness(img).enhance(
        2 + strength / 2
    )

    return img


def denoise(img):

    time.sleep(2)

    img = img.filter(ImageFilter.MedianFilter(size=3))

    img = img.filter(ImageFilter.SMOOTH)

    return img

# -------------------------------------------------
# ЗАГРУЗКА ФОТО
# -------------------------------------------------

uploaded = st.file_uploader(

    "📷 Загрузите фотографию",

    type=["jpg", "jpeg", "png"]

)
# -------------------------------------------------
# ОТОБРАЖЕНИЕ ФОТО
# -------------------------------------------------

if uploaded is not None:

try:
    image = Image.open(uploaded).convert("RGB")
except Exception as e:
    st.error(f"Ошибка открытия изображения: {e}")
    st.stop()    

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Исходное изображение")
        st.image(image, use_container_width=True)

    with col2:

        st.subheader("✨ Результат")

        if st.button("🚀 Обработать фотографию"):

            progress = st.progress(0)

            with st.spinner("AI анализирует изображение..."):

                progress = st.progress(0, text="Обработка...")
                
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1, text=f"AI {i+1}%")

                if mode == "🚀 Улучшение фото":
                    result = ai.enhance(image)

                elif mode == "👶 Омоложение":
                    result = ai.rejuvenate(image)
                elif mode == "🖼 Восстановление":
                    result = ai.restore(image)

                elif mode == "🎨 Улучшение цветов":
                    result = ai.colors(image)

                elif mode == "✨ Повышение резкости":
                    result = ai.sharpen(image)
                elif mode == "📸 Удаление шума":
                    result = denoise(image)

                else:
                    result = image.copy()

            st.success("✅ Обработка завершена!")

            st.image(result, use_container_width=True)

            # Сохраняем результат в session_state
            st.session_state["result"] = result

        else:
            st.info("Выберите режим слева и нажмите «Обработать фотографию».")
# -------------------------------------------------
# СКАЧИВАНИЕ РЕЗУЛЬТАТА
# -------------------------------------------------

if "result" in st.session_state:

    st.divider()

    st.subheader("📥 Скачать обработанное изображение")

    buffer = BytesIO()

    st.session_state["result"].save(
        buffer,
        format="PNG"
    )

    st.download_button(
        label="💾 Скачать PNG",
        data=buffer.getvalue(),
        file_name="AI_Photo_Result.png",
        mime="image/png"
    )

# -------------------------------------------------
# ИНФОРМАЦИЯ
# -------------------------------------------------

st.divider()

with st.expander("ℹ О приложении"):

    st.markdown("""
### AI Photo Editor PRO

Возможности текущей версии:

- 🚀 Улучшение фотографии
- 👶 Омоложение (демо)
- 🖼 Восстановление старых фото
- 🎨 Улучшение цветов
- ✨ Повышение резкости
- 📸 Удаление шума

---

В следующих версиях планируется:

- 🤖 Настоящее AI-омоложение
- 😁 Отбеливание зубов
- 💄 AI-макияж
- 💇 Замена прически
- 👁 Удаление мешков под глазами
- 😎 Удаление морщин
- 📈 Увеличение разрешения до 4K
- 🌅 Замена фона
- 🎭 Face Swap
- 🎬 AI-видео

""")

# -------------------------------------------------
# ФУТЕР
# -------------------------------------------------

st.markdown("---")

st.caption("© 2026 AI Photo Editor PRO")
