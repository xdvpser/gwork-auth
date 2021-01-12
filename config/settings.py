import os

from config.dev import DevSettings
from config.prod import ProdSettings

DEBUG = os.environ.get("FASTAPI_DEBUG", True)

if DEBUG:
    settings = DevSettings()
else:
    settings = ProdSettings()
