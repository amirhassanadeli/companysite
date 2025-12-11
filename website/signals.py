from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from website.models import TeamMember


@receiver(post_save, sender=User)
def manage_team_member(sender, instance, created, **kwargs):
    """
    مدیریت خودکار TeamMember بر اساس is_staff
    ✔ ساخت خودکار عضو تیم
    ✔ جلوگیری از ایجاد تکراری
    ✔ حذف اتوماتیک هنگام خارج شدن از تیم
    """

    # کاربر جدید ایجاد شد
    if created:
        if instance.is_staff:
            TeamMember.objects.get_or_create(user=instance)
        return

    # کاربر قبلاً وجود داشته → وضعیت تغییر کرده

    if instance.is_staff:
        # اگر عضو نیست → بساز
        TeamMember.objects.get_or_create(user=instance)
    else:
        # اگر عضو هست → حذف کن
        TeamMember.objects.filter(user=instance).delete()
