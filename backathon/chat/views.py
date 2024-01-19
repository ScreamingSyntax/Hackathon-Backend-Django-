# myapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import nltk
import numpy as np
import re
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances
from nltk.corpus import stopwords
import json
import random
from rest_framework.views import APIView


# Load dataset and perform necessary preprocessing
with open('dataset.json', 'r') as file:
    data = json.load(file)

def load_dataset():
    dataframe = pd.json_normalize(data['intents'])
    return dataframe

df = load_dataset()

def data_cleaning(df):
    nan_value = df.isna().sum
    df = df.dropna()
    return df


def text_normalization(text):
    text = str(text).lower()
    spl_char_text = re.sub(r'[^a-z\s]', '', text)
    tokens = nltk.word_tokenize(spl_char_text)
    
    lema = WordNetLemmatizer()
    tags_list = nltk.pos_tag(tokens, tagset=None)
    
    lema_words = []
    for token, pos_token in tags_list:
        if pos_token.startswith('V'):
            pos_value = 'v'
        elif pos_token.startswith('J'):
            pos_value = 'a'
        elif pos_token.startswith('R'):
            pos_value = 'r'
        else:
            pos_value = 'n'
        
        lenna_token = lema.lemmatize(token, pos_value)
        lema_words.append(lenna_token)
        
    return " ".join(lema_words)
df = data_cleaning(df)
df['lemmatized_text'] = df['patterns'].apply(text_normalization)

cv = CountVectorizer()
df_bow = pd.DataFrame(cv.fit_transform(df['lemmatized_text']).toarray(), columns=cv.get_feature_names_out())

def index_value_(dataframe_bow, question):
    question_lemma = text_normalization(remove_stopwords(question))
    question_bow = cv.transform([question_lemma]).toarray()
    cosine_value = 1 - pairwise_distances(dataframe_bow, question_bow, metric='cosine')
    index_value = cosine_value.argmax()
    
    return index_value, cosine_value

def remove_stopwords(question):
    A = []
    b = ""
    question = question.split()
    
    for i in question:
        i = i.lower()
        if i in stop:
            continue
        else:
            A.append(i)
        b = " ".join(A)
    return b

stop = stopwords.words('english')
class ChatView(APIView):
      def post(self,request,*args, **kwargs):
            if request.method == 'POST':
                print(request.data)
                user_input = request.POST.get('user_input', '').strip()
                if user_input == 'exit':
                    return JsonResponse({'response': 'Goodbye!'})
                elif not user_input:
                    return JsonResponse({'response': 'Please add a question.'})

                index, cosine_value = index_value_(df_bow, user_input)

                if cosine_value.max() <= 0:
                    return JsonResponse({'response': "Unfortunately, I don't have the information to answer that question. If you have another inquiry or provide more details, I'll do my best to assist you!"})
                else:
                    responses = df['responses'].loc[index]
                    output = random.choice(responses)
                    return JsonResponse({'response': output})

            return render(request, 'chatbot.html')
