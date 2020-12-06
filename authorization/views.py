from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def authorization(request):
    if request.method == "GET":
        return render(request, 'auth/index.html', {})
    elif request.method == "POST":
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            request.session['did_tried'] = 1
            return render(request, 'auth/index.html', {})
