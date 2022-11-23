import requests
import json
import spacy
#import spacy_streamlit
from collections import Counter
from string import punctuation
#import ru_core_news_lg


def summarization_sbercloud(text):
    url = "https://api.aicloud.sbercloud.ru/public/v2/summarizator/predict"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'instances': [
            {
                'text': text,
                'num_return_sequences': 100,
                'length_penalty': 10
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.loads(response.text)


def summarization_spacy(text, percent_of_text_sum=50):
    #nlp = spacy_streamlit.load_model("ru_core_news_lg")
    #nlp = ru_core_news_lg.load()
    nlp = spacy.load("ru_core_news_lg")
    # токенизация
    keywords = []
    tags = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    doc = nlp(text.replace('\n', '').replace('. ', '.').replace('.', '. ').replace('? ', '?').replace('?', '? ').replace('! ', '!').replace('!', '! '))
    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in tags):
            keywords.append(token.text)
    # нормализация частоты слов
    word_freq = Counter(keywords)
    max_freq = Counter(keywords).most_common(1)[0][1]
    for w in word_freq:
        word_freq[w] = (word_freq[w] / max_freq)
    # важность предложений
    sent_power = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in word_freq.keys():
                if sent in sent_power.keys():
                    sent_power[sent] += word_freq[word.text]
                else:
                    sent_power[sent] = word_freq[word.text]
    summary = []
    sorted_x = sorted(sent_power.items(), key=lambda kv: kv[1], reverse=True)
    counter = 0

    max_sents = len(sorted_x)
    limitSentences = round(max_sents * percent_of_text_sum / 100)

    if limitSentences != 0:
        for i in range(len(sorted_x)):
            summary.append(str(sorted_x[i][0]).capitalize())

            counter += 1
            if (counter >= limitSentences):
                break

        # восстановление порядка предложений
        restored_sents_summary = []
        for sent in doc.sents:
            for sum_sent in summary:
                if (str(sum_sent) == str(sent)):
                    restored_sents_summary.append(sum_sent)
                    break
        return ' '.join(summary)
    return ' '

