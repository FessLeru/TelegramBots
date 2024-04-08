import random

from aiogram import Router, Dispatcher, Bot, F, filters
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.methods import edit_message_text, edit_message_reply_markup

import datetime
import time
import asyncio
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio

token = ''
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

router = Router()


class Halls(CallbackData, prefix='hall'):
    hall: int


def first_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Second hall', callback_data=Halls(hall=2).pack())
    builder.button(text='Exit', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()


def second_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='third', callback_data=Halls(hall=3).pack())
    builder.adjust(1)
    return builder.as_markup()


def third_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='fourth', callback_data=Halls(hall=4).pack())
    builder.button(text='Exit', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()


def fourth_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Exit', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()


def start_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Entry', callback_data='entry')
    builder.adjust(1)
    return builder.as_markup()


@router.message(Command('start'))
async def start(msg: Message):
    await msg.answer('Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!', reply_markup=first_kb())


@router.callback_query(Halls.filter())
async def hall(query: CallbackQuery):
    num = int(query.data.split(':')[1])
    if num == 1:
        await query.message.edit_text(f'Вы в зале под номером {num}', reply_markup=first_kb())
    elif num == 2:
        await query.message.edit_text(f'Вы в зале под номером {num}', reply_markup=second_kb())
    elif num == 3:
        await query.message.edit_text(f'Вы в зале под номером {num}', reply_markup=third_kb())
    elif num == 4:
        await query.message.edit_text(f'Вы в зале под номером {num}', reply_markup=fourth_kb())


@router.callback_query(F.data == 'exit')
async def exit(query: CallbackQuery):
    await query.message.edit_text('Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!',
                                  reply_markup=start_kb())


@router.callback_query(F.data == 'entry')
async def ch_start(query: CallbackQuery):
    await query.message.edit_text('Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!',
                                  reply_markup=first_kb())


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
