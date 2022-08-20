from .base import env


SERVICE_USERS_API_BASE_URL = env.str("SERVICE_USERS_API_BASE_URL", default="http://0.0.0.0:8000")
