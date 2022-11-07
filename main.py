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

if file is not None:
    temp = tempfile.NamedTemporaryFile(mode="wb")
    bytes_data = file.getvalue()
    temp.write(bytes_data)
    obj_response = uploadToBucketAndGetPath('itis', temp.name)

    resultText = func_speech(obj_response)
    st.write(resultText)

    resultSummarizationSpacy = summarization_spacy(resultText, percent_of_text_sum)
    st.write(str(resultSummarizationSpacy))

    #TODO: аннотирование текста


    

