import telebot
import imaplib
import email
from email.header import decode_header

# اطلاعات شما
API_TOKEN = '8169736246:AAE03pNj6oiVUB8Bn3TrcK3YeiFnX1Okrfw'
EMAIL_USER = 'آدرس_ایمیل_شما@gmail.com'
EMAIL_PASS = 'رمز_۱۶_رقمی_گوگل' 

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "ربات ایمیل شما در Render فعال شد! 🚀\nبرای چک کردن ایمیل: /check")

@bot.message_handler(commands=['check'])
def check(message):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        _, messages = mail.search(None, "ALL")
        ids = messages[0].split()
        if ids:
            _, data = mail.fetch(ids[-1], "(RFC822)")
            for part in data:
                if isinstance(part, tuple):
                    msg = email.message_from_bytes(part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    bot.send_message(message.chat.id, f"👤 فرستنده: {msg.get('From')}\n📌 موضوع: {subject}")
        else:
            bot.send_message(message.chat.id, "ایمیلی یافت نشد.")
        mail.logout()
    except Exception as e:
        bot.send_message(message.chat.id, f"خطا: {str(e)}")

bot.infinity_polling()
