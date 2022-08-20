from .base import env


MONGO_DB_NAME = env.str("MONGO_DB_NAME", default="crypto_alfred_db")
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://0.0.0.0:27017")
