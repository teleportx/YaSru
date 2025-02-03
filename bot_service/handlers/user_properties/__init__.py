from aiogram import Router

from . import analytics
from . import export
from . import settings

router = Router()

router.include_router(analytics.router)
router.include_router(export.router)
router.include_router(settings.router)
