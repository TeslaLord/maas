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
    plt.pie(values, labels=courses)
    plt.title("UNIT TEST - 3 Scores")
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut1pb.save(curr.aoi+'ut3b.png', content_file2)
    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    plt.pie(values1, labels=courses1)
    plt.title("UNIT TEST - 3 Scores")
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut2pb.save(curr.aoi+'ut3b.png', content_file2)
    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    plt.pie(values2, labels=courses2)
    plt.title("UNIT TEST - 3 Scores")
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut3pb.save(curr.aoi+'ut3b.png', content_file2)
    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    plt.bar(values, courses, color='r',
            edgecolor='grey', label='UT1')
    plt.bar(values1, courses1, color='g',
            edgecolor='grey', label='UT2')
    plt.bar(values2, courses2, color='b',
            edgecolor='grey', label='UT3')
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
