<div align="center">

<img src="assets/banner.svg" alt="envguard" width="100%">

<br>

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-0-22c55e?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-8b5cf6?style=for-the-badge)

### کلید و توکنت رو قبل از اینکه همه‌ی دنیا ببینن پیدا کن 🛡️

</div>

---

<div dir="rtl">

## 😱 ماجرا چیه؟

یه لحظه بی‌دقتی و `API key` اصلی‌ت می‌ره روی گیتهاب. ربات‌ها توی چند ثانیه پیداش می‌کنن و فاکتور سرور بیت‌کوین‌کَنی ارسال می‌شه برای تو! 💸

**envguard** یه اسکنر کوچولوئه که پروژه‌ت رو می‌گرده و هر چی بوی راز بده رو نشونت می‌ده، **قبل از کامیت**.

<img src="assets/features.svg" alt="features" width="100%">

## 🔍 چی رو پیدا می‌کنه؟

| نوع | مثال |
|---|---|
| 🔑 کلید AWS | `AKIA...` |
| 🐙 توکن GitHub | `ghp_...` |
| 💬 توکن Slack | `xoxb-...` |
| 🌐 کلید Google API | `AIza...` |
| 💳 کلید Stripe | `sk_live_...` |
| 🤖 توکن ربات تلگرام | `123456789:AA...` |
| 🗝️ کلید خصوصی | `-----BEGIN PRIVATE KEY-----` |
| 🎫 JWT | `eyJ...` |
| 🙈 پسورد و سکرت هاردکد شده | `password = "..."` |
| 🧬 رشته‌های مشکوکِ پرآنتروپی | کلیدهای رندوم بدون الگوی مشخص |
| 📄 فایل `.env` | که نباید توی ریپو باشه |

## 🚀 شروع سریع

نصب نمی‌خواد! فقط یه فایله:

```bash
git clone https://github.com/CyberLoop-dev/envguard.git
cd envguard

# اسکن پوشه‌ی فعلی
python envguard.py

# اسکن یه پروژه‌ی دیگه
python envguard.py ~/projects/my-app

# فقط چیزایی که می‌خوای کامیت کنی
python envguard.py --staged
```

## 🪝 قفل خودکار روی کامیت

یه بار این رو بزن توی ریپوی خودت:

```bash
python /path/to/envguard.py --install-hook
```

از این به بعد اگه کامیتت راز داشته باشه، **گیت جلوش رو می‌گیره** و می‌گه کجا گند زدی. 😎

## 🖥️ خروجی چه شکلیه؟

```text
config/settings.py
  ✖ AWS Access Key          line 12        AKIA••••••••••••Q7XZ
  ✖ Hardcoded Secret        line 31        pass••••••••••••ord1

.env
  ✖ Env file in repo        file           remove it & add to .gitignore

3 potential secret(s) in 148 files.
```

مقدار واقعی هیچ‌وقت چاپ نمی‌شه؛ فقط یه نسخه‌ی ماسک‌شده نشون داده می‌شه. 🙈

## 🤫 آلارم اشتباه؟

توی همون خط کامنت `envguard:ignore` بذار تا ساکت بشه.

## ⚙️ گزینه‌ها

| گزینه | کارش |
|---|---|
| `--staged` | فقط فایل‌های استیج‌شده |
| `--json` | خروجی JSON برای CI و اسکریپت |
| `--install-hook` | نصب pre-commit hook |

اگه چیزی پیدا بشه، برنامه با کد خروجی `1` تموم می‌شه؛ پس به‌راحتی توی CI هم جا می‌شه.

## 🗺️ نقشه‌ی راه

- [ ] فایل کانفیگ برای قوانین دلخواه
- [ ] اسکن تاریخچه‌ی گیت
- [ ] قالب GitHub Action

## ⚠️ یه نکته‌ی مهم

اگه کلیدی لو رفته، فقط پاک کردنش از کد کافی نیست. **حتماً همون کلید رو باطل (revoke) و یه کلید جدید بساز.**

## 💜 حمایت

اگه به دردت خورد یه ⭐ بهم بده؛ انرژی می‌ده برای ساختن پروژه‌های بعدی!

License: [MIT](LICENSE)

</div>
