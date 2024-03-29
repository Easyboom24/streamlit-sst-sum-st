import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import streamlit as st
import json

def FireBase_Push(date, percentSum, textLength, CheckBoxes, timeYandex):
    cred = credentials.Certificate(json.loads(st.secrets["KEY_FIREBASE"]))
    try:
        firebase_admin.initialize_app(cred)
    except:
        print("Already connected")
    if not percentSum:
        percentSum = null
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
    cred = credentials.Certificate(json.loads(st.secrets["KEY_FIREBASE"]))
    try:
        firebase_admin.initialize_app(cred)
    except:
        print("Already connected")
    ref = db.reference(path="/Analitics", url="https://streamlit-sst-sum-default-rtdb.firebaseio.com") 
    return ref.get()
