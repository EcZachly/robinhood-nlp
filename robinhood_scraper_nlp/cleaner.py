import nltk
import string
import re
nltk.download('stopwords')
BAD_CHARACTERS = ['#', '@']


def remove_punctuation(line):
    return line.translate(str.maketrans('', '', string.punctuation)).replace('"', '')


def de_emojify(inputString):
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', inputString)  # no emoji


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


class ContentCleaner:
    @classmethod
    def clean_text(cls, input_text):

        stopwords = nltk.corpus.stopwords.words('english')
        cleaned_input = de_emojify(decontracted(input_text.lower())) #making all of the words lowercase in order to standardize our data
        words = cleaned_input.split()
        cleaned_words = []
        for word in words:
            cleaned_word = remove_punctuation(word)
            if not any(character in word for character in BAD_CHARACTERS) \
                    and cleaned_word not in stopwords:
                cleaned_words.append(cleaned_word)
        return ' '.join(cleaned_words)




