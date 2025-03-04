from aiogram.fsm.state import State,StatesGroup

class waiting(StatesGroup):
    waiting_a_message = State()