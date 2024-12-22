from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

#управление состанянием
class Form(StatesGroup):
    first_city = State()
    end_city = State()
    additional_cities = State()
