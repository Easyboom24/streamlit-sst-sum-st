from speechToText import func_speech
from boto_file import uploadToBucketAndGetPath
import streamlit as st
import tempfile
#from summarization import summarization_sbercloud

from summarization import summarization_spacy
#import os
#os.system("python -m spacy download ru_core_news_lg")


percent_of_text_sum = st.slider(label="Процент сокращения текста", min_value=0, max_value=100, value=50)
file = st.file_uploader(label="Загрузите аудиозапись")

if file is not None:
    temp = tempfile.NamedTemporaryFile(mode="wb")
    bytes_data = file.getvalue()
    temp.write(bytes_data)
    obj_response = uploadToBucketAndGetPath('itis', temp.name)

    resultText = func_speech(obj_response)
    st.write(resultText)

    #TODO: Сделать ползунок для выбора процента
    #TODO: преобразовывать процент в количество предложений исходя из максимального из resultText
    #TODO: подгрузить модель python -m spacy download ru_core_news_lg
    #resultSummarizationSbercloud = summarization_sbercloud(resultText)
    #st.text(str(resultSummarizationSbercloud['predictions']))

    resultSummarizationSpacy = summarization_spacy(resultText, percent_of_text_sum)
    st.text(str(resultSummarizationSpacy))


    

