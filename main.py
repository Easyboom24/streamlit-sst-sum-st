from speechToText import func_speech
from boto_file import uploadToBucketAndGetPath
import streamlit as st
import streamlit_analytics as sta
# import streamlit.components.v1 as components
import tempfile
# from summarization import summarization_sbercloud

from summarization import summarization_spacy
from annotation import get_annotation

# import os
# os.system("python -m spacy download ru_core_news_lg")

# components.html("""
# <!-- Google tag (gtag.js) -->
# <script async src="https://www.googletagmanager.com/gtag/js?id=G-CH2M532WGY"></script>
# <script>
#   window.dataLayer = window.dataLayer || [];
#   function gtag(){dataLayer.push(arguments);}
#   gtag('js', new Date());
#
#   gtag('config', 'G-CH2M532WGY');
# </script>
# """)

with sta.track():
    percent_of_text_sum = st.slider(label="Процент сокращения текста", min_value=0, max_value=100, value=50)
    file = st.file_uploader(label="Загрузите аудиозапись")

    options = st.multiselect(
        'Выберите, что вы хотите выделить в тексте:',
        [
            'Личности, имена 🔴',
            'Компании, организации 🟡',
            'Места, локации 🔵',
            'Деньги, валюта 🟢',
            'Даты 🟣'
        ]
    )
    st.header('Выберите, что вы хотите выделить в тексте:')
    names = st.checkbox('Личности, имена 🔴')
    orgs = st.checkbox('Компании, организации 🟡')
    locs = st.checkbox('Места, локации 🔵')
    money = st.checkbox('Деньги, валюта 🟢')
    dates = st.checkbox('Даты 🟣')

    buttonActivation = st.button('Запуск обработки')

    if file is not None and buttonActivation:
        with st.spinner('Обработка текста...'):
            temp = tempfile.NamedTemporaryFile(mode="wb")
            bytes_data = file.getvalue()
            temp.write(bytes_data)
            obj_response = uploadToBucketAndGetPath('itis', temp.name)

            st.header("Исходный текст")
            resultText = func_speech(obj_response)
            st.write(resultText)

            st.header("Сокращенный текст")
            resultSummarizationSpacy = summarization_spacy(resultText, percent_of_text_sum)
            st.write(str(resultSummarizationSpacy))

            st.header("Текст с выделенными фрагментами")
            resultAnnotation = get_annotation(str(resultSummarizationSpacy), names, orgs, locs, money, dates)
            st.markdown(resultAnnotation, unsafe_allow_html=True)
