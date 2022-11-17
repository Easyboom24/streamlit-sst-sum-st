from speechToText import func_speech
from boto_file import uploadToBucketAndGetPath
import streamlit as st
import streamlit_analytics as sta
# import streamlit.components.v1 as components
import tempfile
# from summarization import summarization_sbercloud
import pathlib
import logging
import shutil
from bs4 import BeautifulSoup

from summarization import summarization_spacy
from annotation import get_annotation

# import os
# os.system("python -m spacy download ru_core_news_lg")

# components.html(
# """
# <!-- Google tag (gtag.js) -->
# <script async src="https://www.googletagmanager.com/gtag/js?id=G-CH2M532WGY"></script>
# <script>
#   window.dataLayer = window.dataLayer || [];
#   function gtag(){dataLayer.push(arguments);}
#   gtag('js', new Date());
#
#   gtag('config', 'G-CH2M532WGY');
# </script>
# """
# )

def inject_ga():
    GA_ID = "249725330"

    # Note: Please replace the id from G-XXXXXXXXXX to whatever your
    # web application's id is. You will find this in your Google Analytics account

    GA_JS = """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-CH2M532WGY"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-CH2M532WGY');
    </script>
    """

    # Insert the script in the head tag of the static template inside your virtual
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID):  # if cannot find tag
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  # recover from backup
        else:
            shutil.copy(index_path, bck_index)  # keep a backup
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_JS)
        index_path.write_text(new_html)


# inject_ga()


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
        ],
    )
    names, orgs, locs, money, dates = False, False, False, False, False

    for option in options:
        if option == 'Личности, имена 🔴':
            names = True
            break
        if option == 'Компании, организации 🟡':
            orgs = True
            break
        if option == 'Места, локации 🔵':
            locs = True
            break
        if option == 'Деньги, валюта 🟢':
            money = True
            break
        if option == 'Даты 🟣':
            dates = True
            break


    # st.header('Выберите, что вы хотите выделить в тексте:')
    # names = st.checkbox('Личности, имена 🔴')
    # orgs = st.checkbox('Компании, организации 🟡')
    # locs = st.checkbox('Места, локации 🔵')
    # money = st.checkbox('Деньги, валюта 🟢')
    # dates = st.checkbox('Даты 🟣')

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
