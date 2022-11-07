from speechToText import func_speech
from boto_file import uploadToBucketAndGetPath
import streamlit as st
import tempfile
#from summarization import summarization_sbercloud

from summarization import summarization_spacy
from annotation import get_annotation
#import os
#os.system("python -m spacy download ru_core_news_lg")


percent_of_text_sum = st.slider(label="Процент сокращения текста", min_value=0, max_value=100, value=50)
file = st.file_uploader(label="Загрузите аудиозапись")

st.header('Выберите, что вы хотите выделить в тексте:')
names = st.checkbox('Личности, имена')
orgs = st.checkbox('Компании, организации')
locs = st.checkbox('Места, локации')
money = st.checkbox('Деньги, валюта')
dates = st.checkbox('Даты')

resultAnnotation = get_annotation('Фридрих Вильгельм Хуго Бусмайер (Буссмейер, нем. Friedrich Wilhelm Hugo Bußmeyer; 26 февраля 1842, Брауншвейг ' \
           '— 1 февраля 1912, Рио-де-Жанейро) — бразильский пианист и композитор немецкого происхождения. Сын певца ' \
           'Брауншвейгской придворной оперы Морица Бусмайера, брат Ханса Бусмайера. Учился у Анри Литольфа и Альберта ' \
           'Метфесселя. С 1860 года гастролировал по Южной Америке, проехав через Бразилию, Уругвай, Аргентину, ' \
           'Чили и Перу (где в 1866 году познакомился с Луи Моро Готтшалком). В 1867 году вернулся в Европу для концертов ' \
           'в Париже, затем отправился в Мексику и к 1868 году добрался до Нью-Йорка, где прожил несколько лет и, ' \
           'в частности, напечатал серию лёгких фантазий на известные оперные темы[4]. В 1874 году окончательно ' \
           'обосновался в Бразилии, первоначально как профессор органа и аккомпанемента в Императорской консерватории, ' \
           'а в 1875 году возглавил придворную капеллу императора Педру II и руководил ею вплоть до падения бразильской ' \
           'монархии в 1889 году.[5] \n Twitter, 200 долларов, 150 р.', names, orgs, locs, money, dates)
st.markdown(resultAnnotation, unsafe_allow_html=True)
if file is not None:
    temp = tempfile.NamedTemporaryFile(mode="wb")
    bytes_data = file.getvalue()
    temp.write(bytes_data)
    obj_response = uploadToBucketAndGetPath('itis', temp.name)

    resultText = func_speech(obj_response)
    st.write(resultText)

    resultSummarizationSpacy = summarization_spacy(resultText, percent_of_text_sum)
    st.write(str(resultSummarizationSpacy))
    
    resultAnnotation = get_annotation(str(resultSummarizationSpacy), names, orgs, locs, money, dates)
    

    #TODO: аннотирование текста


    

