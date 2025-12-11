document.addEventListener("DOMContentLoaded", () => {

    window.showMessage = (message, type = "success") => {

        document.querySelectorAll(".app-toast").forEach(e => e.remove());

        const box = document.createElement("div");
        box.className = "app-toast";
        box.style = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 100000;
            background: ${type === "success" ? "#22c55e" : "#ef4444"};
            color: white;
            padding: 12px 18px;
            border-radius: 10px;
            font-size: 15px;
            font-family: Vazirmatn, sans-serif;
            box-shadow: 0 6px 14px rgba(0,0,0,0.25);
            opacity: 0;
            transform: translateX(60px);
            transition: .3s;
        `;
        box.innerHTML = message;
        document.body.appendChild(box);

        setTimeout(() => {
            box.style.opacity = "1";
            box.style.transform = "translateX(0)";
        }, 20);

        setTimeout(() => {
            box.style.opacity = "0";
            box.style.transform = "translateX(60px)";
            setTimeout(() => box.remove(), 300);
        }, 4000);
    };

    const form = document.getElementById("contactForm");
    if (!form) return;

    const submitBtn = document.getElementById("submitBtn");

    form.addEventListener("submit", e => {
        e.preventDefault();

        submitBtn.disabled = true;
        submitBtn.innerHTML = "در حال ارسال…";

        document.querySelectorAll(".error-text").forEach(e => e.innerHTML = "");

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        })
            .then(res => res.json())
            .then(data => {

                if (data.success) {
                    showMessage(" پیام شما با موفقیت ارسال شد", "success");
                    form.reset();
                    return;
                }

                if (data.errors) {
                    Object.entries(data.errors).forEach(([field, err]) => {
                        const el = document.getElementById(field + "Error");
                        if (el) el.innerHTML = err;
                        showMessage(err, "error");
                    });
                }
            })
            .catch(() => showMessage("❗ خطا در ارتباط با سرور", "error"))
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = "ارسال پیام";
            });
    });

    if (window.djangoMessages) {
        window.djangoMessages.forEach(m => showMessage(m.text, m.tag));
    }

    function showTab(tabId) {
        document.getElementById("contactTab").style.display = (tabId === 'contactTab') ? "block" : "none";
        document.getElementById("jobTab").style.display = (tabId === 'jobTab') ? "block" : "none";

        document.getElementById("tab-contact-btn").classList.toggle("active", tabId === 'contactTab');
        document.getElementById("tab-job-btn").classList.toggle("active", tabId === 'jobTab');
    }


});
