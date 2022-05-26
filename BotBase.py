from aiogram import Bot, Dispatcher, types
from States import States # States.py

class BotBase:

    bot: Bot = None # bot
    dp: Dispatcher = None # dispatcher

class AdminBotBase(BotBase):

    states: States = None # states
    admin_password: str = "" # admin password
    admin_username: str = "NOT REGISTERED" # admin username
    admin_id: int = -1 # admin id

    def __init__(self, bot: Bot,
                       dp: Dispatcher, 
                       states: States,
                       admin_password: str,
                       admin_username: str = "",
                       admin_id: str = "") -> None:
        self.bot = bot
        self.dp = dp
        self.states = states
        self.admin_password = admin_password
        self.admin_username = admin_username
        self.admin_id = admin_id

    async def show_admin_username(self, message: types.Message) -> None: # showing admin username
        await message.answer(self.admin_username)
    
    async def show_admin_id(self, message: types.Message) -> None: # show admin id
        await message.answer(self.admin_id)

    async def show_admin(self, message: types.Message) -> None: # show admin username and id
        await message.answer(f"Username: @{self.admin_username}\nID: {self.admin_id}")

    async def admin_message(self, message: types.Message) -> None:
        if self.admin_id == message.from_user.id:
            await message.answer("You is already an admin")
        else:
            await message.answer("Enter an admin password")
            await self.dp.current_state(user=message.from_user.id).set_state(self.states.admin)

    async def admin_command(self, message: types.Message) -> None: # working with admin command
        match message.get_args():
            case "username":
                await self.show_admin_username(message)
            case "id":
                await self.show_admin_id(message)
            case "show":
                await self.show_admin(message)
            case _:
                await self.admin_message(message)

    async def admin_message_state_admin(self, message: types.Message) -> None: # working with messages with admin state
        password = message.text
        if password == self.admin_password:
            self.admin_username = message.from_user.username
            self.admin_id = message.from_user.id
            await message.answer("You become an admin")
        else:
            await message.answer("Uncorrect password. Try with /admin command again")
        await self.dp.current_state(user=message.from_user.id).reset_state()

    async def review_command(self, message: types.Message) -> None: # working with review command
        await message.answer("Give all your review in one message")
        await self.dp.current_state(user=message.from_user.id).set_state(self.states.review)

    async def review_to_admin(self, message: types.Message) -> None: # giving review to admin
        review_username: str = ""
        if bool(message.from_user.username) == True:
            review_username = "@" + message.from_user.username
        else:
            review_username = '"' + message.from_user.first_name + '"'
        await self.bot.send_message(self.admin_id, f"New review from {review_username}:")
        await self.bot.send_message(self.admin_id, message.text)
        await self.dp.current_state(user=message.from_user.id).reset_state()
        await message.answer(message.from_user.id, "Gave to admin:)")


class BotBaseCommands(BotBase):

    start_message: list = [] # start messages
    help_message: list = [] # help messages
    about_message: list = [] # about messages
    test_message: list = [] # test messages

    def __init__(self, bot: Bot, dp: Dispatcher, 
                 start_message: list = [], 
                 help_message: list = [], 
                 about_message: list = [], 
                 test_message: list = []) -> None:
        self.bot = bot
        self.dp = dp
        self.start_message = start_message
        self.help_message = help_message
        self.about_message = about_message
        self.test_message = test_message

    async def start_command(self, message: types.Message) -> None: # working with start command
        for m in self.start_message:
            await message.answer(m)

    async def help_command(self, message: types.Message) -> None: # working with help command
        for m in self.help_message:
            await message.answer(m)

    async def about_command(self, message: types.Message) -> None: # working with about command
        for m in self.about_message:
            await message.answer(m)

    async def test_command(self, message: types.Message) -> None: # working with test command
        for m in self.test_message:
            await message.answer(m)