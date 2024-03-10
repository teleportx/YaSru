import asyncio
from datetime import datetime, timedelta

import pytz
from aiogram import Bot
from loguru import logger
from tortoise.expressions import Q

import config
import db
import setup_logger
from db.ToiletSessions import SretSession, SretType
from utils import send_srat_notification

setup_logger.__init__('Notify Service')


async def end_loop():
    while True:
        delete_time = datetime.now(pytz.UTC) - timedelta(hours=1)
        autoend_time = datetime.now(pytz.UTC) - timedelta(minutes=10)
        sessions = (SretSession
                    .filter(Q(Q(start__lte=delete_time), Q(start__lte=autoend_time, autoend=True), join_type='OR'))
                    .filter(sret_type__in=[SretType.SRET, SretType.DRISHET], end=None))

        async for session in sessions:
            if delete_time >= session.start:
                await session.delete()
                continue

            session.end = datetime.now()
            await session.save()

            await send_srat_notification.send(await session.user, 0)

        await asyncio.sleep(60)


async def main():
    await db.init()

    bot = Bot(
        token=config.Telegram.token,
        parse_mode='markdown',
    )
    config.bot = bot

    await end_loop()


if __name__ == "__main__":
    asyncio.run(main())