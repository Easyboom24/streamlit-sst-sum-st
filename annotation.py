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
def get_annotation(text, names = True, orgs = True, locs = True, money = True, dates = True):
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)

    names_extractor = NamesExtractor(morph_vocab)
    money_extractor = MoneyExtractor(morph_vocab)
    dates_extractor = DatesExtractor(morph_vocab)
    addr_extractor = AddrExtractor(morph_vocab)

    output = []

    doc = Doc(text)
    doc.segment(segmenter)
    print("\nОсновные имена собственных")
    if names or orgs or locs:
        doc.tag_ner(ner_tagger)
        for elem in doc.spans:
            if elem.type == "PER" and names:
                output.append([elem.start, elem.stop, elem.type])
            elif elem.type == "LOC" and locs:
                output.append([elem.start, elem.stop, elem.type])
            elif elem.type == "ORG" and orgs:
                output.append([elem.start, elem.stop, elem.type])
    #doc.ner.print() #Получение о"сновных имен собственных (имена, организации, места или локации)

    if (money):
        for elem in list(money_extractor(text)): #Денег
            output.append([elem.start, elem.stop, "Money"])
    if (dates):
        for elem in list(dates_extractor(text)):  # Даты
            output.append([elem.start, elem.stop, "Date"])

#    if (address):
#        for elem in list(addr_extractor(text)): # Адреса
#            if (elem.fact.type != 'село'):
#                output.append([elem.start, elem.stop, "Address"])
    output.sort(key=lambda elem: elem[0])

    doc.ner.print()
    i = len(output) - 1
    end = 0
    edited_text = ""
    for elem in output:
        start = elem[0]
        stop = elem[1]
        type = elem[2]
        edited_text += text[end:start] + "<span type=\"" + type + "\">" + text[start:stop] + "</span>"
        end = stop
    return edited_text
