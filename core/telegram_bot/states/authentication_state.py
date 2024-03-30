from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.methods import EditMessageText
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from telegram_bot.bot import bot
from telegram_bot.lexicon.authentication import AUTHENTICATION_TEXT
from telegram_bot.keyboards.authentication_keyboard import (
    inline_keyboard_authentication_cancel,
    inline_keyboard_authentication
)



authentication_state_router = Router()



async def send_update_message(chat_id, message_id, text, keyboard=inline_keyboard_authentication_cancel) -> None:
    """
    Асинхронная функция для отправки обновленного сообщения с возможностью изменения текста и клавиатуры.

    Parameters:
    - chat_id: Идентификатор чата, в который отправляется сообщение.
    - message_id: Идентификатор сообщения, которое необходимо обновить.
    - text: Текст для обновления сообщения.
    - keyboard: Клавиатура для обновленного сообщения. По умолчанию используется клавиатура inline_keyboard_user_add_cancel.

    Returns:
    - None
    """
    # Отправка запроса на изменение текста и клавиатуры сообщения
    await bot(EditMessageText(
        text=text,
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=keyboard
    ))


class FSMAuthenticationForm(StatesGroup):
    LOGIN = State()
    PASSWORD = State()


@authentication_state_router.callback_query(F.data.in_('authentication_user_state_cancel'), ~StateFilter(default_state))
async def authentication_user_state_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text = AUTHENTICATION_TEXT['cmd_start_not_authentication'],
        reply_markup = inline_keyboard_authentication
    )
    
    await state.clear()
    await callback.answer()


@authentication_state_router.callback_query(F.data.in_('authentication_user_state_login'))
async def authentication_user_continue(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text = AUTHENTICATION_TEXT['authentication_user_state_login'],
        reply_markup = inline_keyboard_authentication_cancel
    )
    
    # Запоминаем ID чата и ID сообщения для его последующего обновления
    await state.update_data(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id
    )
    
    await state.set_state(state=FSMAuthenticationForm.LOGIN)
    
    await callback.answer()


@authentication_state_router.message(StateFilter(FSMAuthenticationForm.LOGIN))
async def state_input_login(message: Message, state: FSMContext):
    await message.delete()
    
    await state.update_data(login=message.text)
    
    data = await state.get_data()
    
    await send_update_message(
        chat_id = data['chat_id'],
        message_id = data['message_id'],
        text = AUTHENTICATION_TEXT['authentication_user_state_password']
    )
    
    await state.set_state(state=FSMAuthenticationForm.PASSWORD)


@authentication_state_router.message(StateFilter(FSMAuthenticationForm.PASSWORD))
async def state_input_password(message: Message, state: FSMContext):
    await message.delete()
    
    await state.update_data(password=message.text)
    
    data = await state.get_data()
    
    await send_update_message(
        chat_id = data['chat_id'],
        message_id = data['message_id'],
        text = AUTHENTICATION_TEXT['authentication_user_state_password']
    )