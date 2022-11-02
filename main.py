import streamlit as st
from speechToText import func_speech
from boto_file import uploadToBucketAndGetPath
import streamlit as st
import tempfile
from pydub import AudioSegment


file = st.file_uploader(label="Загрузите аудиозапись")

if file is not None:
    temp = tempfile.NamedTemporaryFile(mode="wb")
    bytes_data = file.getvalue()
    temp.write(bytes_data)
    fileName =AudioSegment.from_mp3(temp.name).export('result.ogg', format='ogg')    
    obj_response = uploadToBucketAndGetPath('itis',fileName)

    resultText = func_speech(obj_response)
    st.text(resultText)


    

