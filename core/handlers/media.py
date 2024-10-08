import asyncio
from typing import List
from aiogram import Bot
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, ReplyKeyboardMarkup
from core.utils.objects import Post


async def send_post(chat: int, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None, deleteMessages: List[int] | None = None):
    text = post_text(post.title, post.price, post.count)
    file_ids = post.file_ids
    msg = await bot.send_photo(chat_id=chat, photo=file_ids[0], caption=text,
                               reply_markup=markup)
    if deleteMessages is None:
        return msg
    for deleteMessage in deleteMessages:
        await bot.delete_message(chat_id=chat, message_id=deleteMessage)
        await asyncio.sleep(0.01)
    return msg


async def edit_post(chat: int, message_id: int, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None, deleteMessages: List[int] | None = None):
    text = post_text(post.title, post.price, post.count)
    media = post_medias(post.file_ids)
    await bot.edit_message_media(chat_id=chat, media=media[0], message_id=message_id)
    await bot.edit_message_caption(chat_id=chat, message_id=message_id,
                                   caption=text, reply_markup=markup)
    if deleteMessages is None:
        return
    for deleteMessage in deleteMessages:
        await bot.delete_message(chat_id=chat, message_id=deleteMessage)
        await asyncio.sleep(0.01)


async def send_detailed_post(chat: int, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None, deleteMessages: List[int] | None = None):
    text = post_text(post.title, post.price, post.count, post.desc, post.tags)
    media = post_medias(post.file_ids)
    media[0].caption = text
    linked_msgs = [await bot.send_media_group(chat_id=chat, media=media)]
    msg = await bot.send_message(chat_id=chat, text='Вам нравится?', reply_markup=markup)
    if deleteMessages is None:
        return msg
    for deleteMessage in deleteMessages:
        await bot.delete_message(chat_id=chat, message_id=deleteMessage)
        await asyncio.sleep(0.01)
    return msg


async def send_post_channel(chat: int, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None, deleteMessages: List[int] | None = None):
    text = post_text(title=post.title, count=post.count, description=post.desc)
    file_ids = post.file_ids
    msg = await bot.send_photo(chat_id=chat, photo=file_ids[0], caption=text, reply_markup=markup)
    if deleteMessages is None:
        return msg
    for deleteMessage in deleteMessages:
        await bot.delete_message(chat_id=chat, message_id=deleteMessage)
        await asyncio.sleep(0.01)
    return msg


def post_text(title: str, price: int | None = None, count: int | None = None, description: str | None = None, tags: List[str] | None = None):
    text = f"<b>{title}</b>\r\n"
    if price is not None:
        text += f"Цена: <i>{price} zł</i>\r\n"
    if count is not None:
        text += f"{count} в наличии\r\n"
    if description is not None:
        text += f"Описание: <i>{description}</i>\r\n"
    if tags is not None:
        text += f"Категории: {(', '.join(['<code>#' + tag.strip() + '</code>' for tag in tags]))}\r\n"
    return text


def post_medias(photos: List[str]):
    return [InputMediaPhoto(type='photo', media=photo) for photo in photos]
