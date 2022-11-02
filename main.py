import streamlit as st
from speechToText import func_speech
from boto_file import uploadToBucketAndGetPath
import streamlit as st
import tempfile

file = st.file_uploader(label="Загрузите аудиозапись")

if file is not None:
    temp = tempfile.NamedTemporaryFile(mode="wb")
    bytes_data = file.getvalue()
    temp.write(bytes_data)
    print(temp)
    obj_response = uploadToBucketAndGetPath('itis',temp.name)

    resultText = func_speech(obj_response)
    print(resultText)


    

