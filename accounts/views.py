from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.cache import cache
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('website:index')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "حساب شما با موفقیت ایجاد شد 🌹")

            next_url = request.GET.get("next")
            return redirect(next_url if next_url else 'website:index')
        else:
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def login_view(request):
    ip = get_client_ip(request)
    fail_count = cache.get(f"login_fail_{ip}", 0)

    if fail_count >= 5:
        messages.error(request, "تلاش‌های ورود بیش از حد — لطفاً ۵ دقیقه بعد تلاش کنید")
        return render(request, "login.html", {"form": LoginForm()})

    if request.user.is_authenticated:
        return redirect('website:index')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]

            login(request, user)
            cache.delete(f"login_fail_{ip}")

            display_name = user.email  # ✅ اصلاح نهایی

            messages.success(request, f"{display_name} عزیز خوش آمدید 🌹")

            next_url = request.GET.get("next")
            return redirect(next_url if next_url else 'website:index')

        else:
            cache.set(f"login_fail_{ip}", fail_count + 1, timeout=300)
            messages.error(request, "ایمیل یا رمز عبور اشتباه است")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "خروج از حساب با موفقیت انجام شد")
    return redirect('website:index')
