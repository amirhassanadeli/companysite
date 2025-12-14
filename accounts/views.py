from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect

from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm


def change_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "برای تغییر رمز عبور باید وارد حساب شوید.")
        return redirect('login')

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # جلوگیری از logout
            messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
            return redirect('website:index')
    else:
        form = ChangePasswordForm(request.user)

    return render(request, 'change_password.html', {
        'form': form
    })


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('website:index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('website:index')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('website:index')
    else:
        form = SignUpForm()

    return render(request, "register.html", {'form': form})


def update_user(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in.")
        return redirect('login')

    form = UpdateUserForm(request.POST or None, instance=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('website:index')

    return render(request, "update_user.html", {'user_form': form})
