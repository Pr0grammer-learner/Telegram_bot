import config
import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from SQLighter import SQLighter

from Mirea_Parser import Mirea
from ChatGPT import ChatGPT
from Translator import Translator_bot
from Weather import Weather

# Задаем уровень логов
logging.basicConfig(level=logging.INFO)

# Инициализируем Бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()

# Инициализируем соединение с БД
db = SQLighter("db.db")

# Инициализируем парсер
ma = Mirea('lastkey.txt')


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # Если пользователя нет в БД, то добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # Если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer("Вы успешно подписались на рассылку!")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # Если пользователя нет в БД, то добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Хорошо, но вы и так не подписаны.")
    else:
        # Если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались от рассылки.")


# Команда перевода
@dp.message_handler(commands=['translate'])
async def unsubscribe(message: types.Message):
    if message.text.strip("/translate") == "":
        await message.answer("Пример использования команды(регистр ВАЖЕН, языки писать первыми двумя заглавными "
                             "буквами):" + "\n" + "/translate RU Вика лучший тестер! EN")
    else:
        await message.answer(Translator_bot.translate(message.text.strip("/translate")))


# Команда погоды
@dp.message_handler(commands=['weather'])
async def unsubscribe(message: types.Message):
    if message.text.strip("/weather") == "":
        await message.answer("Пример использования команды(регистр не важен:" + "/weather Москва")
    else:
        await message.answer(Weather.weather_check(message.text.strip("/weather")))


# Проверяем наличие новых новостей и делаем рассылки
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        # Проверяем наличие новых новостей
        new_news = ma.new_news()

        if new_news:
            # Если новости есть, переворачиваем список и итерируем
            new_news.reverse()
            for nw in new_news:
                # Парсим инфу о новой новости
                nfo = ma.news_info()

                # Получаем список подписчиков бота
                subscribtions = db.get_subscriptions()

                # Отправляем всем новость
                for s in subscribtions:
                    await bot.send_message(
                        s[1],
                        nfo['tittle'] + "\n" + nfo['text'] + "\n\n" + nfo['link']
                    )

                # Обновляем ключ
                ma.update_lastkey(nfo['id'])


# Chat GPT
@dp.message_handler()
async def echo(message: types.Message):
    answer = ChatGPT.Ask(message.text)
    await message.answer(answer.choices[0].message.content)


# Запускаем лонг поллинг
if __name__ == '__main__':
    loop.create_task(scheduled(10))  # НЕ ЗАБУДЬ ПОМЕНЯТЬ ВРЕМЯ 10 СЕКУНД ДЛЯ ТЕСТА
    executor.start_polling(dp, skip_updates=True)
