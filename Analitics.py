from FireBase import FireBase_Get
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def getAnalitics():
    cleanData = FireBase_Get()
    df = pd.DataFrame({
        "Дата": [],
        "Процент сокращения": [],
        "Длина текста": [],
        "Имена": [],
        "Организации": [],
        "Локации": [],
        "Деньги": [],
        "Даты": [],
        "Время работы SpeechKit": []
        })
    
    
    arrayData = cleanData.items()
    for elem in arrayData:
        df = df.append(elem[1], ignore_index=True)
    df["Имена"].astype(int)
    df["Организации"].astype(int)
    df["Без выделений"] = ((df["Имена"] == 0) & 
                          (df["Организации"] == 0) & 
                          (df["Локации"] == 0) & 
                          (df["Деньги"] == 0) & 
                          (df["Даты"] == 0))
    
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, figsize=(9, 25))
    
    #Гистограмма для чекбоксов (одна, по y  доля использований, по x все чекбоксы)
    ax1.bar(['Имена','Организации', 'Локации', 'Деньги', 'Даты', 'Без выделений'], height=[(sum(df["Имена"] == 1)/len(df)) * 100, 
                                   (sum(df["Организации"] == 1)/len(df)) * 100, 
                                   (sum(df["Локации"] == 1)/len(df)) * 100,
                                   (sum(df["Деньги"] == 1)/len(df)) * 100,
                                   (sum(df["Даты"] == 1)/len(df)) * 100,
                                   (sum(df["Без выделений"] == 1)/len(df)) * 100])
    ax1.set_ylabel("Процент от общего использования")
    ax1.set_title('Использование выделений в тексте')
    
    ax2.hist(data=df, x ="Длина текста", bins=15)
    ax2.set_title('Количество обрабонного текста по его длине')
    ax2.set_xlabel("Длина текста")
    ax2.set_ylabel("Количество обработок по этой длине")
    
    ax3.hist(data=df, x ="Процент сокращения", bins= 10)
    ax3.set_title('Количество обрабонного текста по проценту сокращения')
    ax3.set_xlabel("Процент сокращения")
    ax3.set_ylabel("Количество обработок по этому проценту")
                                             
    ax4.plot("Длина текста", "Время работы SpeechKit", data=df)
    ax4.set_title('Время работы Yandex SpeechKit в зависимости от количества символов')
    ax4.set_xlabel("Количество символов")
    ax4.set_ylabel("Время работы SpeechKit, сек")
    st.write(fig)
    
    #Средняя длина текста - просто вывод
    #Гистограмма по длине текста с разбросом в 100-200 символов (по количеству использований)
    st.write("Среднее значение обработанной длины текста: " + str(round(df["Длина текста"].mean(), 2)))
    #Аналогично с процентом сокращения
    st.write("Средний процент сокращения: " + str(round(df["Процент сокращения"].mean(), 2)))
'''
 plt.bar([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], width=10, height=
            [sum(df["Процент сокращения"] < 11),
             sum((df["Процент сокращения"] > 10) & (df["Процент сокращения"] < 21)),
             sum((df["Процент сокращения"] > 20) & (df["Процент сокращения"] < 31)),
             sum((df["Процент сокращения"] > 30) & (df["Процент сокращения"] < 41)),
             sum((df["Процент сокращения"] > 40) & (df["Процент сокращения"] < 51)),
             sum((df["Процент сокращения"] > 50) & (df["Процент сокращения"] < 61)),
             sum((df["Процент сокращения"] > 60) & (df["Процент сокращения"] < 71)),
             sum((df["Процент сокращения"] > 70) & (df["Процент сокращения"] < 81)),
             sum((df["Процент сокращения"] > 80) & (df["Процент сокращения"] < 91)),
             sum(df["Процент сокращения"] > 90)])
    plt.xticks([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"])
'''
    
#Время работы SpeechKit в зависимости от длины текста (График, где x - длина текста, а y Время работы speechkit),
#plt.hist(data=df, x="Длина текста", y)
#plt.show()
