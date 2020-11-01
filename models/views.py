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
import cv2
import numpy as np
from PIL import Image
from TwitterAPI import *


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

        form = SpeechForm(request.POST, request.FILES)
        print(request.FILES)
        if request.FILES:
            print("HJADJHDSAJHDKJASKDHSKADJHKSAJDHKSJADH")
            opened_text_file = open(
                request.FILES['text_file'].temporary_file_path(), 'r')
            my = opened_text_file.read()
            opened_text_file.close()
            file_var = "For the File: " + str(request.FILES['text_file'])
        else:
            my = request.POST['speech_text']
            file_var = request.POST['speech_text']
        language = 'en'
        myob = gTTS(text=my, lang=language, slow=True)
        myob.save("static/speech/sample.mp3")
        context = {'form': form, 'myob': myob,
                   'input': file_var, 'post': True,
                   }

        return render(request, 'models/text_to_speech.html', context)
    else:
        form = SpeechForm()
    return render(request, 'models/text_to_speech.html', {'form': form})


def speech_to_text(request):
    if request.method == 'POST':
        form = TextForm(request.POST, request.FILES)
        r = sr.Recognizer()
        AUDIO_FILE = request.FILES['audio_file']

        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)
        output = r.recognize_google(audio)
        context = {'input': 'files', 'output': output, 'form': form}
        return render(request, 'models/speech_to_text.html', context)
    else:
        form = TextForm()
        return render(request, 'models/speech_to_text.html', {'form': form})


def pdf(request):
    if request.method == 'POST':
        """FUNCTION TO SHOW THE IMAGE"""
        def show_img(img_list):
            for j, img in enumerate(img_list):
                cv2.imshow(str(j), img)
                cv2.waitKey()

        """FUNCTION TO READ THE IMAGE"""

        def Resize_and_read(crt_imgs):
            for i, im in enumerate(crt_imgs):

                im = cv2.imread(im, -1)
                height, width, *_ = im.shape
                im = cv2.resize(im, None, fx=2, fy=2,
                                interpolation=cv2.INTER_CUBIC)
                correct_images[i] = im

        """FUNCTION TO CONVERT THE IMAGE INTO GRAY SCALE"""

        def convert_gray(crt_images, Gray):
            for i, img in enumerate(crt_images):
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                Gray.append(img)

        """FUNCTION TO SMOOTHEN THE IMAGE"""

        def smoothen_image(gray_img, smooth_img):
            for j, img in enumerate(gray_img):
                img = cv2.resize(img, None, fx=0.25, fy=0.25,
                                 interpolation=cv2.INTER_CUBIC)
                img = cv2.medianBlur(img, 7)
                smooth_img.append(img)

        """FUNCTION TO DETECT THE EDGES"""

        def edge_image(smooth_img, edge_img):
            for j, img in enumerate(smooth_img):
                img = cv2.Canny(img, 25, 200)
                img = cv2.resize(img, None, fx=4, fy=4,
                                 interpolation=cv2.INTER_CUBIC)
                edge_img.append(img)

        """TO FIND THE CONTOURS OF THE IMAGE"""

        def find_img_contours(edge_list, contours_list):
            for img in edge_list:
                contours, hierarchy = cv2.findContours(
                    img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                contours_list.append(contours)

        """TO DRAW THE REQUIRED CONTOURS"""

        def draw_img_contours(all_cnts, imgs, requi_coordinates):
            for j, cnts in enumerate(all_cnts):
                req_cnt = None

                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

                for cnt in cnts:
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                    if len(approx) == 4:
                        req_cnt = approx
                        requi_coordinates.append(req_cnt)
                        break
                cv2.drawContours(imgs[j], [req_cnt], -1, (255, 0, 255), 4)

        """FUNCTION TO PREPROCESS THE REQUIRED CO-ORDINATES"""

        def req_coor_pre(r_c, r_c_l):
            for k, co in enumerate(r_c):
                a_x = co[0][0][0]
                a_y = co[0][0][1]
                a = [a_x, a_y]

                b_x = co[1][0][0]
                b_y = co[1][0][1]
                b = [b_x, b_y]

                c_x = co[2][0][0]
                c_y = co[2][0][1]
                c = [c_x, c_y]

                d_x = co[3][0][0]
                d_y = co[3][0][1]
                d = [d_x, d_y]

                lst = [a, b, c, d]
                lst = sorted(lst, key=lambda x: x[0])
                if lst[0][1] <= lst[1][1]:
                    top_left = lst[0]
                    bottom_left = lst[1]
                else:
                    top_left = lst[1]
                    bottom_left = lst[0]

                if lst[2][1] <= lst[3][1]:
                    top_right = lst[2]
                    bottom_right = lst[3]
                else:
                    top_right = lst[3]
                    bottom_right = lst[2]

                r_c_l.append([top_left, top_right, bottom_left, bottom_right])

        """FUNCTION TO FIND HEIGHT AND WIDTH OF NEW WINDOW"""

        def new_window(cor_list, n_h_a_w):
            for cor in cor_list:
                width = cor[1][0] - cor[0][0]
                height = cor[2][1] - cor[0][1]
                new_width = (width / (width + height)) * 2000
                new_height = (height / (width + height)) * 2000
                n_h_a_w.append([int(new_height), int(new_width)])

        """FUNCTION TO CHANGE PERSPECTIVE"""

        def perspective_change(ori_img, cors, hei_and_wid, new_img):
            for j, img in enumerate(ori_img):
                pt_1 = np.float32(cors[j])
                pt_2 = np.float32(
                    [[0, 0], [hei_and_wid[j][1], 0], [0, hei_and_wid[j][0]], [hei_and_wid[j][1], hei_and_wid[j][0]]])
                matrix = cv2.getPerspectiveTransform(pt_1, pt_2)
                result = cv2.warpPerspective(
                    ori_img[j], matrix, (hei_and_wid[j][1], hei_and_wid[j][0]))
                new_img.append(result)

        """FUNCTION TO SHARPEN THE IMAGE"""

        def sharp_image(img_list, sh_img_list):
            for img in img_list:
                filter = np.array(
                    [[-1 / 8, -1 / 8, -1 / 8], [-1 / 8, 16 / 8, -1 / 8], [-1 / 8, -1 / 8, -1 / 8]])
                s_img = cv2.filter2D(img, -1, filter)
                sh_img_list.append(s_img)

        """FUNCTION FOR ADAPTIVE THRESHOLDING"""

        def adaptive_threshold_image(img_list, res_img):
            for img in img_list:
                thres_img = cv2.adaptiveThreshold(
                    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 20)
                res_img.append(thres_img)

        """FUNCTION TO CONVERT THE LIST OF ARRAYS INTO IMAGE"""

        def pil_convert(array, img_list):
            for img in array:
                im = Image.fromarray(img)
                img_list.append(im)

        """FUNCTION TO CONVERT THE LIST OF IMAGES TO PDF AND SAVE THE PDF FILE"""

        def img_to_pdf(img_list, file_name):
            im1 = img_list[0]
            if len(img_list) > 1:

                im1.save("static/speech/"+file_name + ".pdf", save_all=True,
                         append_images=img_list[1:])
            else:
                im1.save("static/speech/"+file_name + ".pdf")

        """GETTING THE IMAGES FROM THE USER"""
        # file_format = input("Enter the file format ")
        # images = input("Enter the name of the images ").split()
        form = ImageForm(request.POST, request.FILES)
        # images =
        correct_images = []
        files = request.FILES.getlist('image_file')
        print(files)
        for file in files:
            image = file.temporary_file_path()
            correct_images.append(image)

        """1.READ IMAGE"""

        Resize_and_read(correct_images)
        # show_img(correct_images)
        correct_images_copy = []
        sharp_image(correct_images, correct_images_copy)
        # show_img(correct_images_copy)

        """2.CONVERTING THE IMAGE INTO GREY SCALE"""

        Gray_img_list = []
        convert_gray(correct_images_copy, Gray_img_list)
        # show_img(Gray_img_list)

        """3.SMOOTHENING THE IMAGE"""

        smooth_img_list = []
        smoothen_image(Gray_img_list, smooth_img_list)
        # show_img(smooth_img_list)

        """4.DETECTING EDGES"""

        edge_img_list = []
        edge_image(smooth_img_list, edge_img_list)
        # show_img(edge_img_list)

        """5.FINDING CONTOURS"""
        All_contours = []
        edge_copied_img_list = edge_img_list.copy()
        find_img_contours(edge_copied_img_list, All_contours)

        """6.DRAW THE CONTOURS"""
        required_cordinates = []
        draw_img_contours(All_contours, correct_images_copy,
                          required_cordinates)
        # show_img(correct_images_copy)

        """7.PREPROCESSING THE REQUIRED CO-ORDINATE"""
        req_coor_list = []
        req_coor_pre(required_cordinates, req_coor_list)

        """8.FINDING THE NEW WINDOW'S HEIGHT AND WIDTH"""
        new_hei_and_wid = []
        new_window(req_coor_list, new_hei_and_wid)

        """9.sharpening the image"""
        sharpened_image = []
        sharp_image(Gray_img_list, sharpened_image)
        # show_img(sharpened_image)

        """10.ADAPTIVE THRESHOLDING"""
        threshold_image = []
        adaptive_threshold_image(sharpened_image, threshold_image)
        # show_img(result_image)

        """11.CHANGING PERSPECTIVE AND ASKING FOR USER'S OPTION"""
        transformed_image = []

        # option = input("Enter your option: 1. original  2. black and white ")

        if request.POST['type'] == 'original':
            perspective_change(correct_images, req_coor_list,
                               new_hei_and_wid, transformed_image)
        elif request.POST['type'] == 'bw':
            perspective_change(threshold_image, req_coor_list,
                               new_hei_and_wid, transformed_image)
        # show_img(transformed_image)

        """12.CONVERTING INTO PIL OBJECT"""
        final_img_list = []
        pil_convert(transformed_image, final_img_list)

        """13.CONVERTING INTO PDF AND SAVING"""
        img_to_pdf(final_img_list, "test")
        context = {
            'form': form,
            'input': True,

        }
        print("successfully converted")
        return render(request, 'models/pdf.html', context)
    else:
        form = ImageForm()
        return render(request, 'models/pdf.html', {'form': form})


def models(request):
    return render(request, 'models/home.html')
