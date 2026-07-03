import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Photo Editor Pro", page_icon="✨")
st.title("✨ AI Photo Editor Pro")

# Выбор инструмента
option = st.sidebar.selectbox(
    "Выберите инструмент:",
    ("Омоложение (CodeFormer)", "Удаление фона (Rembg)", "Улучшение (Upscale)")
)

st.write(f"### Вы работаете в режиме: {option}")

# Ссылки на готовые демо-пространства (они работают 24/7)
if option == "Омоложение (CodeFormer)":
    components.iframe("https://sczhou-codeformer.hf.space", height=800)
elif option == "Удаление фона (Rembg)":
    components.iframe("https://abhishek-rembg.hf.space", height=800)
elif option == "Улучшение (Upscale)":
    components.iframe("https://nateraw-real-esrgan.hf.space", height=800)
