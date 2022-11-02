import requests
import streamlit as st

def func_speech(audio):
    header = {'Authorization':'Api-Key {}'.format(st.secrets["API_KEY_FOR_CLOUD"])}
    bodyReq = {
        "config": {
            "specification": {
            "languageCode": "ru-RU",  # Язык, для которого будет выполнено распознавание. Значение по умолчанию — русский язык.
            "model": "general",    #Языковая модель, которую следует использовать при распознавании.Значение по умолчанию: general     
            "profanityFilter": "true",  #фильтр ненормативной лексики
            "literature_text" : "true", #расстановка пунктуации
            "audioEncoding": "MP3",
            #"sampleRateHertz": "integer"   Частота дискретизации передаваемого аудио. Для MP3 не обязателен
        }
    },
    "audio": {
        "uri": audio
    }}
    res = requests.post("https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize",json=bodyReq, headers=header)
    data = res.json()
    operationId = data['id']

    while True:
        res = requests.get('https://operation.api.cloud.yandex.net/operations/{operationId}'.format(operationId=operationId),
        headers=header)
        res = res.json()
        if res['done']: break

    result = ""
    for chunk in res['response']['chunks']:
        result += chunk['alternatives'][0]['text'] + "\n"

    return result