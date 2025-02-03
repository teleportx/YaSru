from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import config
from db.User import User
from keyboards import settings_keyboard
from utils.verify_name import verify_name

router = Router()


class ChangeAutoendTimeStates(StatesGroup):
    write_time = State()


class ChangeNameStates(StatesGroup):
    write_name = State()


def generate_menu_text(user: User) -> str:
    text = (f'<b>Настройки</b>\n'
            f'Ник: <i>{user.name}</i>\n'
            f'Автозавершение: <i>{["Выкл", "Вкл"][user.autoend]}</i>\n')

    if user.autoend:
        text += f'Время автозавершения: <i>{user.autoend_time} мин</i>'
    return text


change_time_text = 'Какое новое время <i>(в минутах)</i> установить для автозавершения?\n\n/cancel Для отмены'
change_name_text = 'Напишите ваш новый никнейм. Учтите, он может состоять только из букв, цифр, пробелов, подчеркиваний и тире.\n\n/cancel Для отмены'


@router.message(Command('settings'))
async def settings(message: types.Message, user: User):
    await message.reply(generate_menu_text(user), reply_markup=settings_keyboard.get(user))


@router.callback_query(settings_keyboard.Settings.filter(F.action == 'autoend'))
async def switch_autoend(callback: types.CallbackQuery, user: User):
    user.autoend = not user.autoend
    await user.save()

    await callback.message.edit_text(generate_menu_text(user), reply_markup=settings_keyboard.get(user))


@router.callback_query(settings_keyboard.Settings.filter(F.action == 'autoendtime'))
async def change_autoend_time(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(change_time_text)

    await state.set_state(ChangeAutoendTimeStates.write_time)
    await state.update_data(last_msg=callback.message.message_id)


@router.message(ChangeAutoendTimeStates.write_time)
async def change_autoend_time_write_time(message: types.Message, user: User, state: FSMContext):
    last_msg_id = (await state.get_data()).get('last_msg')

    await message.delete()
    if not message.text.isnumeric():
        await message.bot.edit_message_text(change_time_text + '\n\nВремя должно быть <b>числом</b>.',
                                            chat_id=message.from_user.id, message_id=last_msg_id)
        return

    if not(3 <= int(message.text) <= config.Constants.srat_delete_time):
        await message.bot.edit_message_text(change_time_text + f'\n\nВремя автозавершения должно быть <b>не меньше 3 и не больше {config.Constants.srat_delete_time} минут.</b>',
                                            chat_id=message.from_user.id, message_id=last_msg_id)
        return

    user.autoend_time = int(message.text)
    await user.save()

    await message.bot.edit_message_text(generate_menu_text(user) + f'\n\nВремя автозаврешения установлено на <i>{user.autoend_time} мин</i>.',
                                        reply_markup=settings_keyboard.get(user),
                                        chat_id=message.from_user.id, message_id=last_msg_id)


@router.callback_query(settings_keyboard.Settings.filter(F.action == 'name'))
async def change_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(change_name_text)

    await state.set_state(ChangeNameStates.write_name)
    await state.update_data(last_msg=callback.message.message_id)


@router.message(ChangeNameStates.write_name)
async def change_name_write_name(message: types.Message, user: User, state: FSMContext):
    last_msg_id = (await state.get_data()).get('last_msg')

    await message.delete()

    if len(message.text) > 129:
        await message.bot.edit_message_text(change_name_text + '\n\nИмя должно быть не длиннее 129 символов.',
                                            chat_id=message.from_user.id, message_id=last_msg_id)
        return

    if not verify_name(message.text):
        await message.bot.edit_message_text(change_name_text + '\n\nИмя не соответствует политике.',
                                            chat_id=message.from_user.id, message_id=last_msg_id)
        return

    user.name = message.text
    await user.save()

    await message.bot.edit_message_text(generate_menu_text(user) + f'\n\nВаше имя установлено на <i>{user.name}</i>.',
                                        reply_markup=settings_keyboard.get(user),
                                        chat_id=message.from_user.id, message_id=last_msg_id)