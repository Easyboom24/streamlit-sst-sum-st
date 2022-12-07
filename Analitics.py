from FireBase import FireBase_Get
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
    
    #Гистограмма для чекбоксов (одна, по y  доля использований, по x все чекбоксы)
    plt.bar(['Имена','Организации', 'Локации', 'Деньги', 'Даты'], height=[(sum(df["Имена"] == 1)/len(df)) * 100, 
                                   (sum(df["Организации"] == 1)/len(df)) * 100, 
                                   (sum(df["Локации"] == 1)/len(df)) * 100,
                                   (sum(df["Деньги"] == 1)/len(df)) * 100,
                                   (sum(df["Даты"] == 1)/len(df)) * 100,])
    plt.ylabel("Процент от общего использования")
    plt.suptitle('Использование выделений в тексте')
    plt.show()
    
    #Средняя длина текста - просто вывод
    #Гистограмма по длине текста с разбросом в 100-200 символов (по количеству использований)
    print("Среднее значение обработанной длины текста: " + str(df["Длина текста"].mean()))
    plt.hist(data=df, x ="Длина текста", bins=15)
    plt.suptitle('Количество обрабонного текста по его длине')
    plt.xlabel("Длина текста в символах")
    plt.ylabel("Количество обработок данной длины")
    plt.show()
    
    #Аналогично с процентом сокращения
    print("Средний процент сокращения: " + str(df["Процент сокращения"].mean()))
    plt.hist(data=df, x ="Процент сокращения", bins= 10)
    plt.suptitle('Количество обрабонного текста по проценту сокращение')
    plt.xlabel("Процент сокращения")
    plt.ylabel("Количество обработок по этому проценту")
    plt.show()    
#Время работы SpeechKit в зависимости от длины текста (График, где x - длина текста, а y Время работы speechkit),
#plt.hist(data=df, x="Длина текста", y)
#plt.plot("Длина текста", "Время работы SpeechKit", data=df)
#plt.show()
