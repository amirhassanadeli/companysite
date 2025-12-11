from django import forms

from accounts.models import User


# =========================
#   REGISTER FORM
# =========================

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
    )
    confirm_password = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["email", "password"]
        widgets = {
            "email": forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not email:
            raise forms.ValidationError("ایمیل نمی‌تواند خالی باشد")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")

        if not p1:
            self.add_error("password", "رمز عبور نمی‌تواند خالی باشد")
            return cleaned_data

        if p1 != p2:
            self.add_error("confirm_password", "رمز عبور و تکرار آن یکسان نیستند")

        if len(p1) < 8:
            self.add_error("password", "رمز عبور باید حداقل ۸ کاراکتر باشد")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


# =========================
#   LOGIN FORM
# =========================
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={"autocomplete": "username", "class": "form-control"})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email", "").strip().lower()
        password = cleaned_data.get("password")

        if not email:
            raise forms.ValidationError("ایمیل الزامی است")

        if not password:
            raise forms.ValidationError("رمز عبور الزامی است")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("اطلاعات ورود صحیح نیست")

        if not user.check_password(password):
            raise forms.ValidationError("اطلاعات ورود صحیح نیست")

        if not user.is_active:
            raise forms.ValidationError("حساب کاربری شما غیر فعال است")

        cleaned_data["user"] = user
        return cleaned_data
