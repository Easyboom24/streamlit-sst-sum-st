import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import streamlit as st
import json
import tempfile

#Функция должна срабатывать каждый раз, когда нажалась кнопка и пошел процесс основной работы
def FireBase_Push(date, percentSum, textLength, CheckBoxes, timeYandex):
    my_str = st.secrets["KEY_FIREBASE"]
    import json,tempfile
    tfile = tempfile.NamedTemporaryFile(mode="w+")
    json.dump(my_str, tfile)
    tfile.flush()
    try:
        firebase_admin.initialize_app(tfile.name)
    except:
        print("Already connected")
    ref = db.reference(path="/Analitics", url="https://streamlit-sst-sum-default-rtdb.firebaseio.com") 
    if (len(CheckBoxes) != 5):
        return "Not this array!"
    else:
        ref.push({
                	"Дата": date,
                    "Процент сокращения": percentSum,
                    "Длина текста": textLength,
                    "Имена": CheckBoxes[0],
                    "Организации": CheckBoxes[1],
                    "Локации": CheckBoxes[2],
                    "Деньги": CheckBoxes[3],
                    "Даты": CheckBoxes[4],
                    "Время работы SpeechKit": timeYandex
                    
                 })
        return "Success"
def FireBase_Get():
    my_str = st.secrets["KEY_FIREBASE"]
    import json,tempfile
    tfile = tempfile.NamedTemporaryFile(mode="w+")
    json.dump(my_str, tfile)
    tfile.flush()
    firebase_admin.initialize_app(tfile.name)
    ref = db.reference(path="/Analitics", url="https://streamlit-sst-sum-default-rtdb.firebaseio.com") 
    return ref.get()

#print(FireBase_Push("01.09.2022", 10, 200, [True, True, False, True, True], 7))
