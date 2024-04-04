from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery
from telegram_bot.filters.filter import AuthenticationStudentFilter
from telegram_bot.eduutils.student_db import get_student_send_personal_data
from telegram_bot.keyboards.student_keyboard import inline_kyboard_panel
from asgiref.sync import sync_to_async

# Инициализация роутера
student_handler = Router()

# Пременить фильтр для всех сообщений, для учеников который аутентифицированы
student_handler.message.filter(AuthenticationStudentFilter())
student_handler.callback_query.filter(AuthenticationStudentFilter())


@student_handler.message(F.text == '/panel')
async def cmd_panel_student(message: Message):
    await message.delete()
    await message.answer(
        text = 'Панель обучающегося',
        reply_markup = inline_kyboard_panel
    )
    

@student_handler.callback_query(F.data.in_('student_send_personal_data'))
async def student_send_personal_data(callback: CallbackQuery):
    personal_data = await sync_to_async(get_student_send_personal_data)(callback.from_user.id)
    
    entities = callback.message.entities or []  # Получение сущностей сообщения (если есть)
    for item in entities:
        if item.type in personal_data.keys():
            personal_data[item.type] = item.extract_from(callback.message.text)  # Извлечение информации из сущностей сообщения
        
    await callback.message.edit_text(
        f'📹 Ваши персональные данные\n'
        f'🔒 Уникальный ID: {html.quote(str(personal_data["id"]))}\n'
        f'🔒 Логин: {html.quote(str(personal_data["login"]))}\n'
        f'🔒 Пароль: {html.quote(str(personal_data["password"]))}\n'
        f'🔒 ФИО: {html.quote(str(personal_data["full_name"]))}\n'
        f'🔒 Телеграм ID: {html.quote(str(personal_data["telegram_id"]))}\n'
        f'🔒 Статус аутентификации: {html.quote(str(personal_data["is_authentication"]))}\n'
        )
    
    await callback.answer()