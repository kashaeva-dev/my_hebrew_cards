import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from asgiref.sync import sync_to_async
from django.core.management import BaseCommand

from conf import settings
from mycards.management.commands.config import logger_config
from mycards.management.commands.keyboards import (
    user_register_keyboard, get_user_main_keyboard,
)
from mycards.models import (
    Client,
)

logger = logging.getLogger('bot_logger')
logging.config.dictConfig(logger_config)

bot = Bot(settings.TG_BOT_TOKEN)
storage=MemoryStorage()
dp=Dispatcher(bot=bot, storage=storage)


class ClientRegisterFSM(StatesGroup):
    personal_info=State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    client, created = await sync_to_async(Client.objects.get_or_create)(
        chat_id=message.from_user.id,
    )
    if created or not client.first_name or not client.last_name:
        await message.answer('🤖 Добро пожаловать в чат-бот\n<b>ИВРИМИЛИЯ</b>\n\n'
                             'Я помогу вам 🧠 запомнить новые слова на иврите 🕎!\n\n'
                             '🎫 Но вначале нужно зарегистрироваться.',
                            parse_mode='HTML',
                            reply_markup=user_register_keyboard,
                            )
    else:
        user_main_keyboard = await get_user_main_keyboard()
        await message.answer('🤖 ГЛАВНОЕ МЕНЮ:',
                             parse_mode='HTML',
                             reply_markup=user_main_keyboard,
                             )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'user_register', state='*')
async def user_register_handler(callback: types.CallbackQuery) -> None:
    await ClientRegisterFSM.personal_info.set()
    await callback.message.edit_text('Для продолжения регистрации введите Ваше имя и '
                                     'фамилию в формате: <b>Имя Фамилия</b>',
                                     parse_mode='HTML',
                                     )


@dp.message_handler(state=ClientRegisterFSM.personal_info)
async def get_personal_info_handler(message: types.Message, state: FSMContext) -> None:
    if message.text.count(' ') != 1:
        await message.answer('Неверный формат ввода. Попробуйте еще раз.\n'
                             'Введите ваше имя и фамилию в формате: <b>Имя Фамилия</b>',
                             parse_mode='HTML',
                             )
        return
    first_name, last_name = message.text.split()

    client, _ = await sync_to_async(Client.objects.get_or_create)(chat_id=message.from_user.id)
    client.first_name = first_name
    client.last_name = last_name
    await sync_to_async(client.save)()
    logger.info(f'first_name: {client.first_name}, last_name: {client.last_name}')
    await bot.send_message(client.chat_id,
                           f'{client.first_name} {client.last_name}, Вы успешно зарегистрированы!',
                           parse_mode='HTML',
                           reply_markup=await get_user_main_keyboard()
                           )
    await state.finish()




class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True)
