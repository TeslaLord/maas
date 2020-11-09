from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
import matplotlib.pyplot as plt
import io
from django.core.files.images import ImageFile
import urllib
import base64
import numpy as np

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for the {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def results(request):
    curr = Profile.objects.filter(user=request.user).first()

    l = eval(curr.ut1)
    plt.clf()
    data = {'IP': l[0], 'MRF': l[1], 'FOC': l[2], 'RA': l[3], 'SAT': l[4]}
    courses = list(data.keys())
    values = list(data.values())
    figure = io.BytesIO()
    fig = plt.subplots(figsize =(6, 6)) 
    plt.bar(courses, values, color='maroon',
            width=0.4)
    plt.xlabel("Courses")
    plt.ylabel("Marks")
    plt.title("UNIT TEST - 1 Scores")
    plt.savefig(figure, format="png")
    content_file = ImageFile(figure)
    curr.ut1p.save(curr.aoi+'ut1.png', content_file)
    plt.clf()

    l1 = eval(curr.ut2)
    data1 = {'IP': l1[0], 'MRF': l1[1],
             'FOC': l1[2], 'RA': l1[3], 'SAT': l1[4]}
    courses1 = list(data1.keys())
    values1 = list(data1.values())
    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize =(6, 6)) 
    plt.bar(courses1, values1, color='maroon',
            width=0.4)
    plt.xlabel("Courses")
    plt.ylabel("Marks")
    plt.title("UNIT TEST - 2 Scores")
    plt.savefig(figure, format="png")
    content_file1 = ImageFile(figure)
    curr.ut2p.save(curr.aoi+'ut2.png', content_file1)
    plt.clf()

    l2 = eval(curr.ut3)
    data2 = {'IP': l2[0], 'MRF': l2[1],
             'FOC': l2[2], 'RA': l2[3], 'SAT': l2[4]}
    courses2 = list(data2.keys())
    values2 = list(data2.values())
    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize =(6, 6)) 
    plt.bar(courses2, values2, color='maroon',
            width=0.4)
    plt.xlabel("Courses")
    plt.ylabel("Marks")
    plt.title("UNIT TEST - 3 Scores")
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut3p.save(curr.aoi+'ut3.png', content_file2)
    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize =(6, 6)) 
    plt.pie(values, labels=courses)
    plt.title("UNIT TEST - 1 Scores")
    plt.legend()
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut1pb.save(curr.aoi+'ut3b.png', content_file2)
    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize =(6, 6)) 
    plt.pie(values1, labels=courses1)
    plt.title("UNIT TEST - 2 Scores")
    plt.legend()
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut2pb.save(curr.aoi+'ut3b.png', content_file2)

    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize =(6, 6)) 
    plt.pie(values2, labels=courses2)
    plt.title("UNIT TEST - 3 Scores")
    plt.legend()
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut3pb.save(curr.aoi+'ut3b.png', content_file2)
    
    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    barWidth = 1
    fig = plt.subplots(figsize =(12, 8)) 
  
    length = [6,12,18,24,30]
    plt.bar([i for i in length], values, color ='maroon', width = barWidth, 
            edgecolor ='grey', label ='UT1') 
    plt.bar([i+1 for i in length], values1, color ='grey', width = barWidth, 
            edgecolor ='grey', label ='UT2') 
    plt.bar([i+2 for i in length], values2, color ='navy', width = barWidth, 
            edgecolor ='grey', label ='UT3') 

    plt.xlabel('Score', fontweight ='bold') 
    plt.ylabel('Subjects in UT', fontweight ='bold') 
    plt.title("UNIT TEST Performance Comparison")
    plt.xticks([i+1 for i in length], 
            ['IP', 'MRF', 'RA', 'SAT', 'FOC']) 
    plt.legend()
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut12.save(curr.aoi+'ut3b.png', content_file2)
    plt.clf()

    context = {'images': [
        curr.ut1p.url, curr.ut2p.url, curr.ut3p.url, curr.ut1pb.url, curr.ut2pb.url, curr.ut3pb.url, curr.ut12.url]}

    print(context)
    return render(request, 'users/results.html', context)


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile successfully Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)
