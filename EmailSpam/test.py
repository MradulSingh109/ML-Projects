import pickle
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
        
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Test with a known spam message
test_msg = "Phony £350 award - Todays Voda numbers ending XXXX are selected to receive a £350 award. If you have a match please call 08712300220 quoting claim code 3100 standard rates app"
transformed = transform_text(test_msg)
vector = tfidf.transform([transformed])
pred = model.predict(vector)[0]
print(f"Prediction: {pred}")  # Should be 1 for spam

# Test with ham
ham_msg = "Come to me right now, Ahmad"
transformed_ham = transform_text(ham_msg)
vector_ham = tfidf.transform([transformed_ham])
pred_ham = model.predict(vector_ham)[0]
print(f"Ham Prediction: {pred_ham}")  # Should be 0

# Test with user input
user_input = input("Enter a message: ")
transformed_user = transform_text(user_input)
vector_user = tfidf.transform([transformed_user])
pred_user = model.predict(vector_user)[0]
print(f"User Prediction: {pred_user}")