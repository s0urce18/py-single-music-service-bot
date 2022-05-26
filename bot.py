# imports ----------------------------------
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Song import Song # Songs.py
from States import States # States.py
from BotBase import AdminBotBase, BotBaseCommands # BotBase.py
import json
# ------------------------------------------

# bot, dispatcher, states and admin base creating -------------
bot_config_file = open("bot_config.json", encoding="utf-8") # opening bot_config.json

"""bot_config.json:
{
    "token": *BOT TOKEN*,
    "admin": {
        "admin_password": *ADMIN PASSWORD*,
        "admin_username": *ADMIN USERNAME*,
        "admin_id": *ADMIN ID*
    },
    "messages": {
        "start_message": [
            *START MESSAGE 1*,
            *START MESSAGE 2*,
            ...
            *START MESSAGE N*
        ],
        "help_message": [
            *HELP MESSAGE 1*,
            *HELP MESSAGE 2*,
            ...
            *HELP MESSAGE N*
        ],
        "about_message": [
            *ABOUT MESSAGE 1*,
            *ABOUT MESSAGE 2*,
            ...
            *ABOUT MESSAGE N*
        ],
        "test_message": [
            *TEST MESSAGE 1*,
            *TEST MESSAGE 2*,
            ...
            *TEST MESSAGE N*
        ]
    }
}
"""

bot_config_dict: dict = json.loads(bot_config_file.read()) # extracting from json to dict
bot_config_file.close() # closing bot_config.json 
bot: Bot = Bot(token=bot_config_dict["token"]) # creating bot
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage()) # creating dispatcher
states: States = States() # creating states
admin_bot_base: AdminBotBase = AdminBotBase(bot, dp, states, **bot_config_dict["admin"]) # creating admin base
bot_base_commands: BotBaseCommands = BotBaseCommands(bot, dp, **bot_config_dict["messages"]) # creating base commands
# -----------------------------------------

# registering admin messages --------------
dp.register_message_handler(admin_bot_base.admin_command, commands=["admin"]) # admin command
dp.register_message_handler(admin_bot_base.admin_message_state_admin, state=states.admin) # working with messages with state admin
dp.register_message_handler(admin_bot_base.review_command, commands=["review"]) # review command
dp.register_message_handler(admin_bot_base.review_to_admin, state=states.review) # giving review to admin
# -----------------------------------------

# registering base commands ---------------
dp.register_message_handler(bot_base_commands.start_command, commands=["start"]) # start command
dp.register_message_handler(bot_base_commands.help_command, commands=["help"]) # help command
dp.register_message_handler(bot_base_commands.about_command, commands=["about"]) # about command
dp.register_message_handler(bot_base_commands.test_command, commands=["test"]) # test command
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
    await message.answer(f"{query}: {song.get_name()}\n" +
                         f"YT Music: {song.get_ytm_link()}\n" +
                         f"Spotify: {song.get_sp_link()}\n" +
                         f"Deezer: {song.get_dz_link()}") # answer