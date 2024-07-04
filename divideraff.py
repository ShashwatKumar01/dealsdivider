import tempfile
from io import BytesIO

from pyrogram import Client, filters, enums
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
import logging
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import asyncio
from quart import Quart
from unshortenit import UnshortenIt

api_id= '26566076'
api_hash= '40ce27837b95819c42cac67b46a2dc2b'
bot_token='6810447810:AAHTehMwBCzhG2Eicu2OBvAnSoo-d9D9bYs'
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define a handler for the /start command
bot = Quart(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

source_channel_id = [-1002110764294]  # Replace with the source channel ID
amazon_id = -1002049093974
flipkart_id = -1002124607504
meesho_id = -1002133412234
ajiomyntra_id= -1002146712649
cc_id= -1002078634799
beauty_id= -1002046497963

amazon_keywords=['amzn','amazon','tinyurl']
flipkart_keywords=['fkrt','flipkart','boat','croma','tatacliq','fktr']
ajio_keywords=['ajiio','myntr','xyxx']
meesho_keywords=['meesho','shopsy','msho']
beauty_keywords=['mamaearth','bombayshavingcompany','beardo','themancompany','wow','nykaa','mCaffeine','Bombay Shaving Company','BSC','TMC','foxtale','facewash','deo','cream','trimmer','bodywash','fitspire','PUER']
# cc_keywords=['axis','hdfc','icici','sbm','sbi','credit','idfc','aubank','hsbc','Axis','Hdfc','Icici','Sbm','Sbi','Credit','Idfc','Aubank','Hsbc',
#             'AXIS','HDFC','ICICI','SBM','SBI','CREDIT','IDFC','AUBANK','HSBC']
cc_keywords=['Apply Now','Lifetime Free','Apply for',' Lifetime free','Benifits','Apply here','Lifetime FREE','ELIGIBILITY','Myzone','Rupay','rupay','Complimentary','Apply from here','annual fee','Annual fee','joining fee']

shortnerfound=['extp','bitli','bit.ly','bitly','bitili']

# tuple(amazon_keywords): amazon_id,
keyword_to_chat_id = {
    tuple(flipkart_keywords): flipkart_id,
    tuple(meesho_keywords): meesho_id,
    tuple(ajio_keywords): ajiomyntra_id,
    tuple(beauty_keywords):beauty_id,
    tuple(cc_keywords):cc_id
}

def extract_link_from_text(text):
    # Regular expression pattern to match a URL
    url_pattern = r'https?://\S+'
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

def unshorten_url(short_url):
    unshortener = UnshortenIt()
    shorturi = unshortener.unshorten(short_url)
    # print(shorturi)
    return shorturi
async def send(id,message):
    Promo = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Deals HUB 🛒", url="https://t.me/addlist/FReIeSd3Hyg5NjJl"),InlineKeyboardButton("PriceHistory Deals 📉", url="https://t.me/+rTx5B9g6XYxmNmE1")],
         [InlineKeyboardButton("Main Channel 🔴", url="https://t.me/+HeHY-qoy3vsxYWU1")]
         ])

    if message.photo:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            await message.download(file_name=temp_file.name)
            with open(temp_file.name, 'rb') as f:
                photo_bytes = BytesIO(f.read())
        await app.send_photo(chat_id=id,photo=photo_bytes,caption=message.caption,caption_entities=message.caption_entities,reply_markup=Promo)




    elif message.text:
        await app.send_message(chat_id=id,text=message.text,entities=message.entities,disable_web_page_preview=True)


@bot.route('/')
async def hello():
    return 'Hello, world!'

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await app.send_message(message.chat.id,"ahaann")


@app.on_message(filters.chat(source_channel_id))
async def forward_message(client, message):
    inputvalue=''
    if message.caption_entities:
        for entity in message.caption_entities:
            if entity.url is not None:
                inputvalue=entity.url
        # print(hyerlinkurl)
        if inputvalue=='':
            text = message.caption if message.caption else message.text
            inputvalue = text
    # if message.photo:
    #     text = message.caption if message.caption else message.text
    #     inputvalue = text
    # elif message.text:
    #     inputvalue = message.text
    # print(inputvalue)
    #
    if message.entities:
        for entity in message.entities:
            if entity.url is not None:
                inputvalue=entity.url
        # print(hyerlinkurl)
        if inputvalue=='':
            text = message.text
            inputvalue = text

    if any(keyword in inputvalue for keyword in shortnerfound):
        print(extract_link_from_text(inputvalue))
        inputvalue= unshorten_url(extract_link_from_text(inputvalue))
        # print(inputvalue)
    # source_link= unshorten_url(extract_link_from_text(inputvalue))


    # if any(keyword in inputvalue for keyword in amazon_keywords):
    #     await send(amazon_id,message)
    #     # await app.forward_messages(amazon_id, from_chat_id=source_channel_id, message_ids=message.id)

    for keywords, chat_id in keyword_to_chat_id.items():
        if any(keyword in inputvalue for keyword in keywords):
            await send(chat_id, message)

@app.on_message(filters.chat(-1001873285810))
async def forward_message2(client, message):

    if message.photo:
        text = message.caption if message.caption else message.text
        inputvalue = text
    elif message.text:
        inputvalue = message.text

    if any(keyword in inputvalue for keyword in shortnerfound):
        inputvalue= unshorten_url(extract_link_from_text(inputvalue))

    if any(keyword in inputvalue for keyword in meesho_keywords):
        await send(meesho_id,message)            
    if any(keyword in inputvalue for keyword in beauty_keywords):
        await send(beauty_id,message)
    # if any(keyword in inputvalue for keyword in ajio_keywords):
    #     await send(ajiomyntra_id,message)

@bot.before_serving
async def before_serving():
    await app.start()


@bot.after_serving
async def after_serving():
    await app.stop()


# if __name__ == '__main__':

    # bot.run(port=8000)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run_task(host='0.0.0.0', port=8080))
    loop.run_forever()
