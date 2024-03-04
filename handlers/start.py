from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from filters.user import UserAuthFilter

router = Router()


@router.message(Command("start"), UserAuthFilter())
async def start(message: types.Message, first_joined: bool):
    if first_joined:
        text = (f'Добро пожаловать в УРА!\n\n'
                f''
                f'*У вас есть четыре действия:*\n'
                f'Я иду срать - начать срать\n'
                f'Я иду ЛЮТЕЙШЕ ДРИСТАТЬ - начать дристать\n'
                f'Я закончил срать - закончить деяние\n'
                f'Я просто пернул - когда вы пердите или закончили деяние неудачно.\n\n'
                f''
                f'Закончить срать можно только тогда когда вы срете, пердеть можно в любое время.')

        await message.answer(text)

    kb = ReplyKeyboardBuilder()

    kb.button(text='Я иду ЛЮТЕЙШЕ ДРИСТАТЬ')
    kb.button(text='Я иду срать')
    kb.button(text='Я закончил срать')
    kb.button(text='Я просто пернул')

    kb.adjust(2)

    await message.reply('Выберете действие.', reply_markup=kb.as_markup())
