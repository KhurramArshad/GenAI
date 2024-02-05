from DataCleanPipeLine import CleanData
from sklearn.feature_extraction.text import TfidfVectorizer


def clean_data_and_get_encoding(path, text_column_name):
    obj = CleanData(path, text_column_name)
    cleaned_text = obj.run()
    tfidf = TfidfVectorizer()
    encodings= tfidf.fit_transform(cleaned_text).toarray()
    vocab = tfidf.get_feature_names_out()
    return {"vocab": vocab, "encodings": encodings}


path = "../data/sample.csv"
text_column_name = "text"

result = clean_data_and_get_encoding(path, text_column_name)
print(result)