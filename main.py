import streamlit as st
from speechToText import func_speech
from boto_file import uploadToBucketAndGetPath
from summarization import summarization_sbercloud
from summarization import summarization_spacy
import streamlit as st
import tempfile



file = st.file_uploader(label="Загрузите аудиозапись")

if file is not None:
    temp = tempfile.NamedTemporaryFile(mode="wb")
    bytes_data = file.getvalue()
    temp.write(bytes_data)
    obj_response = uploadToBucketAndGetPath('itis', temp.name)

    resultText = func_speech(obj_response)
    st.text(resultText)

    resultSummarizationSbercloud = summarization_sbercloud(resultText)
    resultSummarizationSpacy = summarization_spacy(resultText, 5)

    st.text(str(resultSummarizationSbercloud['predictions']))
    st.text(str(resultSummarizationSpacy))


    

