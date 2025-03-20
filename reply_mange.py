import asyncio
import logging
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest
from pymongo import MongoClient
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import Message
import pyromod 
import pyromod.listen
import faulthandler
from pyrogram.types import ReplyKeyboardMarkup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_id = 28610306

api_hash = "3f57cc57f8883bd604baf3b814ffe023"
bot_token = "8185892232:AAG-WUeHNlwGQu_agcekfr9i6k8UWxUPbvY"

ADMINS = [7419979232,7473872971]

app = Client('Replies', api_id, api_hash, bot_token= bot_token)


@app.on_message(filters.private & ~filters.bot)
async def reply_handler(client, message):
  print(message.text)
  for i in ADMINS:    
    try:
      await app.copy_message(chat_id=i, from_chat_id = message.chat.id, message_id = message.id,
                             reply_markup = InlineKeyboardMarkup([
                               [InlineKeyboardButton(f"💬 Reply {message.chat.id}", callback_data=f"reply_{message.chat.id}")]
                             ]))
    except Exception as e:
      print(e)


@app.on_callback_query(filters.regex("^reply_"))
async def reply_to_user(client, callback_query):
    """ Handle reply button click and send a response to the user. """
    admin_id = callback_query.from_user.id
    user_id = int(callback_query.data.split("_")[1])

    reply = await client.ask(chat_id = admin_id,
        text=f"✏️ **Please send the message you want to reply with.**",
        filters=filters.text & ~filters.bot
    )

    # Wait for the admin's reply
    # reply = await client.ask(admin_id)

    # Send the reply to the user
    await client.send_message(
        chat_id=user_id,
        text=f"{reply.text}"
    )

    await callback_query.message.reply_text(f"✅ Message sent to the {user_id} user.")

app.run()
