import logging
import re

from django.core.cache import cache
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from website.models import Contact, TeamMember, Service, Project, JobRequest

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
#  Utility Functions
# ------------------------------------------------------------------------------

def _get_client_ip(request):
    """ تشخیص دقیق IP حتی پشت کلودفلر و پروکسی """
    for key in ["HTTP_CF_CONNECTING_IP", "HTTP_X_FORWARDED_FOR", "REMOTE_ADDR"]:
        ip = request.META.get(key)
        if ip:
            return ip.split(",")[0].strip()
    return "0.0.0.0"


def _validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def _rate_limited(key_prefix, ip, max_attempts=5, timeout=300):
    """
    بررسی محدودیت تعداد تلاش‌ها برای جلوگیری از اسپم
    """
    key = f"{key_prefix}_{ip}"
    attempts = cache.get(key, 0)

    if attempts >= max_attempts:
        return True, attempts

    cache.set(key, attempts + 1, timeout=timeout)
    return False, attempts


def _reset_rate_limit(prefix, ip):
    cache.delete(f"{prefix}_{ip}")


def _sanitize(text):
    """ ساده‌ترین نوع پاکسازی برای جلوگیری از XSS """
    return text.strip().replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------------------------
#   Home + Business Card Views
# ------------------------------------------------------------------------------

def home(request):
    context = {
        "services": Service.objects.filter(is_active=True).order_by("order"),
        "projects": Project.objects.order_by("order", "-is_featured"),
        "team": TeamMember.objects.select_related("user").order_by("order"),
    }
    return render(request, "index.html", context)


def business_card(request):
    return render(request, "_business_card.html")


# ------------------------------------------------------------------------------
#   Contact Form View
# ------------------------------------------------------------------------------

@csrf_protect
def contact_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    ip = _get_client_ip(request)

    # --- Anti-Spam Protection ---
    spam, attempts = _rate_limited("contact_fail", ip)
    if spam:
        return JsonResponse({
            "success": False,
            "error": "درخواست‌های بیش از حد — لطفاً چند دقیقه صبر کنید"
        }, status=429)

    # --- Extract Data ---
    name = _sanitize(request.POST.get("name", ""))
    email = _sanitize(request.POST.get("email", "").lower())
    phone = _sanitize(request.POST.get("phone", ""))
    message = _sanitize(request.POST.get("message", ""))

    # --- Validation ---
    errors = {}

    if not name:
        errors["name"] = "نام الزامی است"

    if not email or not _validate_email(email):
        errors["email"] = "ایمیل معتبر نیست"

    if not phone.isdigit():
        errors["phone"] = "شماره تلفن معتبر وارد کنید"

    if not message:
        errors["message"] = "متن پیام الزامی است"

    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    # --- Duplicate Check ---
    if Contact.objects.filter(email=email).exists():
        return JsonResponse({"success": False, "errors": {"email": "این ایمیل تکراری است"}}, status=400)

    if Contact.objects.filter(phone=phone).exists():
        return JsonResponse({"success": False, "errors": {"phone": "این شماره تکراری است"}}, status=400)

    # --- Save ---
    Contact.objects.create(
        user=request.user if request.user.is_authenticated else None,
        name=name,
        email=email,
        phone=phone,
        message=message,
        ip=ip,
    )

    _reset_rate_limit("contact_fail", ip)
    logger.info(f"📩 Contact from: {name} ({email}) — IP: {ip}")

    return JsonResponse({"success": True}, status=200)


# ------------------------------------------------------------------------------
#   Job Request View
# ------------------------------------------------------------------------------

@csrf_protect
def job_request(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    ip = _get_client_ip(request)

    # --- Anti-spam ---
    spam, attempts = _rate_limited("job_fail", ip)
    if spam:
        return JsonResponse({
            "success": False,
            "error": "تلاش‌های بیش از حد — لطفاً چند دقیقه بعد دوباره امتحان کنید"
        }, status=429)

    # --- Extract Data ---
    name = _sanitize(request.POST.get("name", ""))
    email = _sanitize(request.POST.get("email", "").lower())
    phone = _sanitize(request.POST.get("phone", ""))
    field = _sanitize(request.POST.get("field", ""))
    message = _sanitize(request.POST.get("message", ""))

    # --- Validation ---
    errors = {}

    if not name:
        errors["name"] = "نام الزامی است"

    if not email or not _validate_email(email):
        errors["email"] = "ایمیل معتبر نیست"

    if not phone.isdigit():
        errors["phone"] = "شماره تلفن معتبر وارد کنید"

    if not field:
        errors["field"] = "انتخاب حوزه همکاری الزامی است"

    if not message or len(message) < 10:
        errors["message"] = "متن پیام باید حداقل ۱۰ کاراکتر باشد"

    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    # --- Save ---
    JobRequest.objects.create(
        user=request.user if request.user.is_authenticated else None,
        name=name,
        email=email,
        phone=phone,
        field=field,
        message=message,
        ip=ip,
    )

    _reset_rate_limit("job_fail", ip)
    logger.info(f"🧑‍💼 Job Request from: {name} – Field: {field} – IP: {ip}")

    return JsonResponse({"success": True}, status=200)
