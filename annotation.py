from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsNERTagger,

    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,

    Doc
)
def get_annotation(text, names, orgs, locs, money, address):
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)
    
    names_extractor = NamesExtractor(morph_vocab)
    money_extractor = MoneyExtractor(morph_vocab)
    dates_extractor = DatesExtractor(morph_vocab)
    addr_extractor = AddrExtractor(morph_vocab)
    
    text = 'Фридрих Вильгельм Хуго Бусмайер (Буссмейер, нем. Friedrich Wilhelm Hugo Bußmeyer; 26 февраля 1842, Брауншвейг ' \
           '— 1 февраля 1912, Рио-де-Жанейро) — бразильский пианист и композитор немецкого происхождения. Сын певца ' \
           'Брауншвейгской придворной оперы Морица Бусмайера, брат Ханса Бусмайера. Учился у Анри Литольфа и Альберта ' \
           'Метфесселя. С 1860 года гастролировал по Южной Америке, проехав через Бразилию, Уругвай, Аргентину, ' \
           'Чили и Перу (где в 1866 году познакомился с Луи Моро Готтшалком). В 1867 году вернулся в Европу для концертов ' \
           'в Париже, затем отправился в Мексику и к 1868 году добрался до Нью-Йорка, где прожил несколько лет и, ' \
           'в частности, напечатал серию лёгких фантазий на известные оперные темы[4]. В 1874 году окончательно ' \
           'обосновался в Бразилии, первоначально как профессор органа и аккомпанемента в Императорской консерватории, ' \
           'а в 1875 году возглавил придворную капеллу императора Педру II и руководил ею вплоть до падения бразильской ' \
           'монархии в 1889 году.[5] \n Twitter, 200 долларов, 150 р.'
    doc = Doc(text)
    doc.segment(segmenter)
    print("\nОсновные имена собственных")
    doc.tag_ner(ner_tagger)
    doc.ner.print() #Получение основных имен собственных (имена, организации, места или локации)
    
    #Получение данных с помощью экстракторов
    # print("\nИмена")
    # for elem in list(names_extractor(text)): #Получение имен
    #     print(elem)
    print("\nДеньги")
    for elem in list(money_extractor(text)): #Денег
        print(elem)
    print("\nДаты")
    for elem in list(dates_extractor(text)): #Дат
        print(elem)
    
    lines = [
        'Россия, Вологодская обл. г. Череповец, пр.Победы 93 б',
        '692909, РФ, Приморский край, г. Находка, ул. Добролюбова, 18',
        'ул. Народного Ополчения д. 9к.3'
    ]
    print("\nАдреса")
    for line in lines:
        print(addr_extractor.find(line))
