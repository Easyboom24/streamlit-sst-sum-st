from speechToText import func_speech
from boto_file import uploadToBucketAndGetPath
import streamlit as st
import tempfile
from summarization import summarization_sbercloud
from summarization import summarization_spacy



file = st.file_uploader(label="Загрузите аудиозапись")

if file is not None:
    temp = tempfile.NamedTemporaryFile(mode="wb")
    bytes_data = file.getvalue()
    temp.write(bytes_data)
    obj_response = uploadToBucketAndGetPath('itis', temp.name)

    resultText = func_speech(obj_response)
    st.text(resultText)

    #TODO: Сделать ползунок для выбора процента
    #TODO: преобразовывать процент в количество предложений исходя из максимального из resultText
    #TODO: подгрузить модель python -m spacy download ru_core_news_lg
    resultSummarizationSbercloud = summarization_sbercloud(resultText)
    resultSummarizationSpacy = summarization_spacy(resultText, 5)

    st.text(str(resultSummarizationSbercloud['predictions']))
    st.text(str(resultSummarizationSpacy))


    

