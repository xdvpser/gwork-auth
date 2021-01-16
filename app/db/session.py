import databases

from config.settings import settings

database = databases.Database(str(settings.SQLALCHEMY_DATABASE_URI))
