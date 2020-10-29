from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render
from textblob import TextBlob
# Create your views here.
from .forms import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import confusion_matrix
import speech_recognition as sr
from gtts import gTTS
import playsound
import os


def sentiment(request):
    if request.method == 'POST':
        feedback = request.POST['sentiment_text']

        blob = TextBlob(feedback)

        form = SentimentForm(request.POST)
        blob = blob.polarity + 1
        context = {'blob': blob, 'form': form,
                   'input': request.POST['sentiment_text']}
        return render(request, 'models/sentiment.html', context)
    else:
        form = SentimentForm()
    return render(request, 'models/sentiment.html', {'form': form})


def category(request):
    if request.method == 'POST':
        data = fetch_20newsgroups()
        data.target_names
        train = fetch_20newsgroups(
            subset='train', categories=data.target_names)
        test = fetch_20newsgroups(subset='test', categories=data.target_names)
        model = make_pipeline(TfidfVectorizer(), MultinomialNB())

        def predict_category(s):
            pred = model.predict([s])
            return train.target_names[pred[0]]
        model.fit(train.data, train.target)
        labels = model.predict(test.data)
        form = CategoryForm(request.POST)
        category_out = predict_category(request.POST['category_text'])
        context = {'category': category_out, 'form': form,
                   'input': request.POST['category_text']}
        return render(request, 'models/category.html', context)
    else:
        form = CategoryForm()
    return render(request, 'models/category.html', {'form': form})


def text_to_speech(request):
    if request.method == 'POST':

        form = SpeechForm(request.POST)
        my = request.POST['speech_text']
        language = 'en'
        myob = gTTS(text=my, lang=language, slow=True)
        myob.save("static/speech/sample.mp3")
        context = {'form': form, 'myob': myob,
                   'input': request.POST['speech_text'], 'post': True}
        return render(request, 'models/text_to_speech.html', context)
    else:
        form = SpeechForm()
    return render(request, 'models/text_to_speech.html', {'form': form})


def speech_to_text(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        r = sr.Recognizer()
        AUDIO_FILE = ('static/speech/'+request.POST['audio_file'])
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)
        output = r.recognize_google(audio)
        context = {'input': request.POST['audio_file'], 'output': output}
        return render(request, 'models/speech_to_text.html', context)
    else:
        form = TextForm()
        return render(request, 'models/speech_to_text.html', {'form': form})


def models(request):
    return render(request, 'models/home.html')
