from django.conf import settings
from django.db import models


class JobRequest(models.Model):
    FIELD_CHOICES = [
        ("ai", "هوش مصنوعی و یادگیری ماشین"),
        ("backend", "برنامه‌نویسی بک‌اند"),
        ("frontend", "برنامه‌نویسی فرانت‌اند"),
        ("ds", "دیتاساینس / تحلیل داده"),
        ("devops", "DevOps"),
        ("uiux", "UI/UX"),
        ("marketing", "مارکتینگ / روابط عمومی"),
        ("other", "سایر"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    message = models.TextField()
    ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_field_display()})"


class Service(models.Model):
    ICON_CHOICES = [
        ('bi-cpu', 'CPU'),
        ('bi-code', 'Programming'),
        ('bi-cloud', 'Cloud'),
        ('bi-database', 'Database'),
        ('bi-robot', 'AI'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    category = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True)
    image = models.ImageField(upload_to='projects/', blank=True)
    demo_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-is_featured', '-created_at']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/', blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.user.email} - {self.position}"


class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_read', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
