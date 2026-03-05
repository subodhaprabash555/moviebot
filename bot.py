import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

BOT_TOKEN = "8642899423:AAH_ay34-6easlS9m1vJRa53zsX2b2NjqEw"
bot = telebot.TeleBot(BOT_TOKEN)

API = "https://api.themoviedb.org/3"
API_KEY = "9749e1cc34cc81122cae6b163608aa03"

WEBSITE = "https://www.moviestream.it.com"

# SEARCH
@bot.message_handler(func=lambda m: True)
def search_movie(message):

    query = message.text

    url = f"{API}/search/multi?api_key={API_KEY}&query={query}"
    data = requests.get(url).json()

    markup = InlineKeyboardMarkup()

    for item in data["results"][:10]:

        title = item.get("title") or item.get("name")
        year = ""

        if item.get("release_date"):
            year = item["release_date"][:4]

        if item.get("first_air_date"):
            year = item["first_air_date"][:4]

        id = item["id"]
        media = item["media_type"]

        markup.add(
            InlineKeyboardButton(
                f"{title} ({year})",
                callback_data=f"{media}_{id}"
            )
        )

    bot.send_message(
        message.chat.id,
        f"""HY !...SUBODHA 
🧑‍💻MOVIE STREAM REQUEST MANAGER🧑‍💻

ඔබගේ ඇතුලත් කිරීම 👉 {query}

පහල ලිස්ට් එකෙන් ඔබට හොයන එක තෝරාගන්න👇


 --👑POWERED BY MOVIE STREAM👑 --""",
        reply_markup=markup
    )


# CLICK RESULT
@bot.callback_query_handler(func=lambda call: True)
def send_movie(call):

    media,id = call.data.split("_")

    if media == "movie":
        url = f"{API}/movie/{id}?api_key={API_KEY}"
    else:
        url = f"{API}/tv/{id}?api_key={API_KEY}"

    data = requests.get(url).json()

    title = data.get("title") or data.get("name","-")

    year = "-"
    if data.get("release_date"):
        year = data["release_date"][:4]

    if data.get("first_air_date"):
        year = data["first_air_date"][:4]

    country = "-"
    if data.get("production_countries"):
        country = data["production_countries"][0]["name"]

    language = "-"
    if data.get("spoken_languages"):
        language = data["spoken_languages"][0]["english_name"]

    runtime = "-"
    if data.get("runtime"):
        runtime = str(data["runtime"])+" min"

    rating = data.get("vote_average","-")

    poster = "https://image.tmdb.org/t/p/w500"+data["poster_path"] if data.get("poster_path") else None

    slug = title.lower().replace(" ","-")

    website_link = f"{WEBSITE}/{slug}-{year}"

    text = f"""
☘️ {title} ({year}) Sinhala Subtitles | සිංහල උපසිරැසි සමඟ

📅 Release : {year}
🌎 Country : {country}
🗣 Language : {language}
🕰 Duration : {runtime}
🏆 IMDB Rating : {rating}

🚀 පහත Quality වලින් සහ Size වලින් ඔබට ලබා ගත හැක 👇

WEBDL
WEB-DL 480p • 850 MB
WEB-DL 720p • 1.7 GB
WEB-DL 1080p • 3.4 GB

✅ Original WEB Quality Updated ✅
"""

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            "🌐 WATCH / DOWNLOAD",
            url=website_link
        )
    )

    bot.send_photo(
        call.from_user.id,
        poster,
        caption=text,
        reply_markup=markup
    )

bot.infinity_polling()