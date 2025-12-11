from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True  # برای کار درست با makemigrations / migrate

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("ایمیل الزامی است")

        # normalize & cleanup
        email = self.normalize_email(email).strip().lower()

        user = self.model(email=email, **extra_fields)

        if not password:
            raise ValueError("پسورد نمی‌تواند خالی باشد")

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("سوپر یوزر باید is_staff=True باشد")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("سوپر یوزر باید is_superuser=True باشد")

        return self.create_user(email=email, password=password, **extra_fields)
