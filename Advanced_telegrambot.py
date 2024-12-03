from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
#توکن ربات و کلیدهای API خود را اینجا قرار دهید
BOT_TOKEN = "YOUR_BOT_TOKEN"
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
TRANSLATE_API_KEY = "YOUR_TRANSLATE_API_KEY"  # اختیاری اگر از API رایگان استفاده می‌کنید

#هندلر دستور شروع
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "سلام! 👋\n"
        "من یک ربات چندکاره هستم. این دستورات رو می‌تونید استفاده کنید:\n"
        "/crypto - دریافت قیمت ارزهای دیجیتال\n"
        "/translate - ترجمه متن\n"
        "/weather - پیش‌بینی آب‌وهوا\n"
        "هر سوالی دارید، بپرسید! 😊"
    )

#هندلر دستور ارزهای دیجیتال
def crypto(update: Update, context: CallbackContext) -> None:
    try:
        #دریافت داده‌ها از API CoinGecko
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
        if response.status_code == 200:
            data = response.json()
            bitcoin_price = data["bitcoin"]["usd"]
            ethereum_price = data["ethereum"]["usd"]
            message = (
                f"💰 قیمت ارزهای دیجیتال:\n"
                f"Bitcoin: ${bitcoin_price}\n"
                f"Ethereum: ${ethereum_price}\n"
            )
        else:
            message = "❌ خطا در دریافت قیمت‌ها. لطفاً دوباره امتحان کنید."
    except Exception as e:
        message = f"❌ خطا: {e}"

    update.message.reply_text(message)

#هندلر دستور وضعیت آب‌وهوا
def weather(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("لطفاً نام شهر را وارد کنید. مثال: /weather Tehran")
        return

    city_name = " ".join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            city = data["name"]
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            message = (
                f"🌤 وضعیت آب‌وهوا در {city}:\n"
                f"دمای فعلی: {temp}°C\n"
                f"توضیحات: {weather_desc}\n"
            )
        else:
            message = "❌ شهر مورد نظر پیدا نشد. لطفاً دوباره تلاش کنید."
    except Exception as e:
        message = f"❌ خطا: {e}"

    update.message.reply_text(message)

#هندلر دستور ترجمه
def translate(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text(
            "لطفاً متن و زبان مقصد را وارد کنید. مثال: /translate hello fa"
        )
        return

    text = " ".join(context.args[:-1])
    target_language = context.args[-1]
    try:
        #استفاده از API LibreTranslate برای ترجمه
        response = requests.post(
            "https://libretranslate.com/translate",
            data={
                "q": text,
                "source": "auto",
                "target": target_language,
            },
        )
        if response.status_code == 200:
            translated_text = response.json()["translatedText"]
            message = f"📝 ترجمه:\n{translated_text}"
        else:
            message = "❌ خطا در ترجمه. لطفاً دوباره تلاش کنید."
    except Exception as e:
        message = f"❌ خطا: {e}"

    update.message.reply_text(message)
# تابع اصلی برای شروع ربات
def main():
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher

    #ثبت هندلرهای دستورات
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("crypto", crypto))
    dispatcher.add_handler(CommandHandler("weather", weather))
    dispatcher.add_handler(CommandHandler("translate", translate))
    #شروع ربات
    updater.start_polling()
    updater.idle()

#اجرای ربات
main()
