
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
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
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from user.models import User
from chat.models import ChatBot
from .serializers import ChatSerializer

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
df_bow = pd.DataFrame(cv.fit_transform(
    df['lemmatized_text']).toarray(), columns=cv.get_feature_names_out())


def index_value_(dataframe_bow, question):
    question_lemma = text_normalization(remove_stopwords(question))
    question_bow = cv.transform([question_lemma]).toarray()
    cosine_value = 1 - \
        pairwise_distances(dataframe_bow, question_bow, metric='cosine')
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
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
        # if request.method == 'POST':
            print(request.data)
            print(request.user.id)
            user_input = request.POST.get('user_input', '').strip()
            if user_input == 'exit':
                return Response({'message': 'Goodbye!'})
            elif not user_input:
                return Response({'message': 'Please add a question.', 'error': 1})

            index, cosine_value = index_value_(df_bow, user_input)

            if cosine_value.max() <= 0:
                return Response({'message': "Unfortunately, I don't have the information to answer that question. If you have another inquiry or provide more details, I'll do my best to assist you!", 'success': 1, 'error': 0})
            else:
                responses = df['responses'].loc[index]
                output = random.choice(responses)
                user_obj = User.objects.get(id=request.user.id)
                dataf = {}
                dataf['user'] = user_obj
                dataf['question'] = user_input
                dataf['answer'] = output
                print("Outputtttttt")
                print(output)
                chat_obj = ChatSerializer(data=dataf)
                if (chat_obj.is_valid()):
                    chat_obj.save()
                else:
                    errors = chat_obj.errors
                    return Response({'message': errors, 'success': 0, 'error': 1})
                return Response({'message': output, 'success': 1})
        # return render(request, 'chatbot.html')

def get_user_id_from_token(authorization_header):
    try:
        # Extract the token from the Authorization header
        token = authorization_header.split()[1]

        # Retrieve the user associated with the token
        token_obj = Token.objects.get(key=token)
        user_id = token_obj.user.id

        return user_id
    except (IndexError, Token.DoesNotExist):
        raise AuthenticationFailed("Invalid token")


class FetchChat(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                user = request.user
                chat = ChatBot.objects.filter(user = user)
                chat_serializer = ChatSerializer(chat, many=True)


                return Response({'success': 1, 'data': chat_serializer.data})
        except Exception as e:
            print(e)
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })