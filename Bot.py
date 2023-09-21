import os
import telebot
from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv

load_dotenv('config.env')
load_dotenv('login.env')
BOT_TOKEN = ${{ secrets.BOT_TOKEN }}
login_email = os.environ.get('EMAIL')
login_pass = os.environ.get('PASS')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I'm your AI bot! How can I assist you today?")

@bot.message_handler(func=lambda msg: True)
def chat_with_bot(message):
    email = login_email
    passwd = login_pass
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    
    # Utilizziamo il testo del messaggio dell'utente come prompt per il chatbot
    user_input = message.text
    prompt = f"User: {user_input}\nAssistant:"
    
    # Ottieni la risposta dal chatbot
    response = chatbot.chat(prompt)
    
    # Rimuovi "<endoftext>" dalla fine della risposta, se presente
    response = response.replace("<|endoftext|>", "")
    
    # Invia la risposta al messaggio dell'utente
    bot.reply_to(message, response)

bot.infinity_polling()
