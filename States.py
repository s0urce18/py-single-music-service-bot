from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    admin = State() # admin state
    review = State() # review state