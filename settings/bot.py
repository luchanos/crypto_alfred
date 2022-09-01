import os

from .base import BASE_PATH, env


TOKEN = env.str("TOKEN")
ADMIN_CHAT_ID = env.str("ADMIN_CHAT_ID", default="362857450")
BASE_TG_URL = env.str("TELEGRAM_BASE_URL", default="https://api.telegram.org/bot")
BOT_TG_URL = "{}{}/".format(BASE_TG_URL, TOKEN)
MAIN_CHAT_ID_DEV = env.str("MAIN_CHAT_ID_DEV", default="-1001590701371")
CHAT_ID_GROUP = env.str("CHAT_ID_GROUP", default="-1001629658747")

I18N_DOMAIN = "crypto_alfred"
LOCALES_DIR = os.path.join(BASE_PATH, "locales")
