# imports ----------------------------------
from aiogram import Bot, Dispatcher, types
from Song import Song # Songs.py
import json
# ------------------------------------------

# bot and dispatcher  creating -------------
bot_config_file = open("bot_config.json") # opening bot_config.json

"""bot_config.json:
{
    "token": *BOT TOKEN*
}
"""

bot_config_dict: dict = json.loads(bot_config_file.read()) # extracting from json to dict
bot_config_file.close() # closing bot_config.json 
bot: Bot = Bot(token=bot_config_dict["token"]) # creating bot
dp: Dispatcher = Dispatcher(bot) # creating dispatcher
# -----------------------------------------

@dp.message_handler()
async def main(message: types.Message) -> None: # answer on all messages
    text: str = message.text # message text
    song: Song = None # object Song
    query: str = "Name" # Query type
    if "deezer" in text: # if it's deezer link
        await message.answer("Finding by Deezer link...")
        song = Song(dz_link=text)
    elif "spotify" in text: # if it's spotify link
        await message.answer("Finding by Spotify link...")
        song = Song(sp_link=text)
    elif "youtube" in text: # if it's youtube link
        await message.answer("Finding by YT Music link...")
        song = Song(ytm_link=text)
    else: # if it's plain query
        await message.answer("Finding by query...")
        song = Song(name=text)
        query = "Query"
    # answer:
    await message.answer(f"{query}: {song.get_name()}\nYT Music: {song.get_ytm_link()}\nSpotify: {song.get_sp_link()}\nDeezer: {song.get_dz_link()}")