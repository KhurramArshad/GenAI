import pandas as pd
import re
import string
from Slangs import slang_dict
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import emoji

# nltk.download('stopwords')

class CleanData:
    def __init__(self, data_path, text_column_name):
        """
        data_path: str (must be only csv file)
        column_name: str (column name of the csv that have text to clean)
        """
        self.data_path = data_path
        self.text_column_name = text_column_name
        self.exclude = string.punctuation

    def read_data(self):
        """This method will read all the data and return text column  of data frame"""
        data = pd.read_csv(self.data_path)
        text_data = data[self.text_column_name]
        return text_data

    def __find_word_starting_with_at(self, string):
        match = re.search(r'@[^ ]*', string)
        if match:
            result_string = re.sub(match.group(), "", string)
            result_string = result_string.strip()
            return result_string
        else:
            return string

    def remove_at_the_rate(self, text_data):
        """Removing all the words that start with @ for example @105860"""
        text_data = text_data.apply(self.__find_word_starting_with_at)
        return text_data

    def convert_to_lowercase(self, text_data):
        """Converting all the text to lower case"""
        text_data = text_data.str.lower()
        return text_data

    def __remove_html_tags(self, text):
        pattern = re.compile('<.*?>')
        return pattern.sub("", text)

    def remove_HTML(self, text_data):
        text_data = text_data.apply(self.__remove_html_tags)
        return text_data

    def __remove_url(self, text):
        pattern = re.compile(r'https?://\S+|www\.\S+')
        return pattern.sub("", text)

    def clean_urls(self, text_data):
        """This method will remove all the web urls from text eg. https://www.google.com"""
        text_data = text_data.apply(self.__remove_url)
        return text_data

    def __remove_punc(self, text):
        for char in self.exclude:
            text = text.replace(char, "")
        return text

    def clean_punctuation(self, text_data):
        """Cleaning Punctuation like !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ from text"""
        text_data = text_data.apply(self.__remove_punc)
        return text_data

    def __chat_slang(self, text):
        new_text = []
        for w in text.split():
            if w.upper() in slang_dict:
                new_text.append(slang_dict[w.upper()])
            else:
                new_text.append(w)
        return " ".join(new_text)

    def convert_slang_to_text(self, text_data):
        """This method will convert slang words into plain english eg. ASAP to as soon as possible"""
        text_data = text_data.apply(self.__chat_slang)
        return text_data

    def __correct(self, text):
        txtblob = TextBlob(text)
        return txtblob.correct().string

    def spell_correct(self, text_data):
        """This method will correct the spellings"""
        text_data = text_data.apply(self.__correct)
        return text_data

    def __remove_stopwords(self, text):
        new_text = []
        for word in text.split():
            if word in stopwords.words("english"):
                new_text.append("")
            else:
                new_text.append(word.strip())
        return " ".join(new_text).replace("   ", "")

    def stopword_removal(self, text_data):
        """Removing words like is, are, am, as, etc."""
        text_data = text_data.apply(self.__remove_stopwords)
        return text_data

    def __remove_emoji(self, text):
        clean_text = emoji.demojize(text)
        return clean_text

    def emoji_removal(self, text_data):
        """Removing emojies"""
        text_data = text_data.apply(self.__remove_emoji)
        return text_data

    def __remove_numeric_and_alphanumeric(self, text):
        cleaned_string = re.sub(r'\b\d+\b|\b\w*\d\w*\b', '', text)
        return cleaned_string

    def remove_digits(self, text_data):
        """Removing numeric and alpha numeric words"""
        text_data = text_data.apply(self.__remove_numeric_and_alphanumeric)
        return text_data

    def run(self):
        text_data = self.read_data()
        text_data = self.remove_at_the_rate(text_data)
        text_data = self.convert_to_lowercase(text_data)
        text_data = self.remove_HTML(text_data)
        text_data = self.clean_urls(text_data)
        text_data = self.clean_punctuation(text_data)
        text_data = self.convert_slang_to_text(text_data)
        text_data = self.spell_correct(text_data)
        text_data = self.stopword_removal(text_data)
        text_data = self.emoji_removal(text_data)
        text_data = self.remove_digits(text_data)
        return text_data