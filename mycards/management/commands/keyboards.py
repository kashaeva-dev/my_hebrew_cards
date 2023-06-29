from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

user_register_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Зарегистрироваться', callback_data='user_register'),
    ],
])


async def get_user_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить слова с сайта', callback_data='add_words_from_site'),
        ],
    ])
