from .base import env


SERVICE_USERS_API_BASE_URL = env.str("SERVICE_USERS_API_BASE_URL", default="http://0.0.0.0:8000")

COIN_API_SERVICE = {
    "base_url": env.str("COIN_API_BASE_URL", default="https://rest.coinapi.io/"),
    "api_key": env.str("COIN_API_KEY", default="F00C0472-C620-42C2-BD2A-24912520F179"),
}
