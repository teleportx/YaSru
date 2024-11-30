from contextlib import asynccontextmanager

from fastapi import FastAPI

import brocker
import db


class Lifespan:
    def __init__(self, *, start_db: bool = False, start_brocker: bool = False):
        self.start_db = start_db
        self.start_brocker = start_brocker

    @asynccontextmanager
    async def __call__(self, app: FastAPI):
        if self.start_db:
            await db.init()

        if self.start_brocker:
            await brocker.init()

        yield
