from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

<<<<<<< HEAD
#управление состанянием
=======
>>>>>>> origin/main
class Form(StatesGroup):
    first_city = State()
    end_city = State()
    additional_cities = State()
