from envparse import Env

env = Env()


COINAPI_SETTINGS = {
    "base_url": env.str("COINAPI_BASE_URL"),
    "api_key": env.str("COINAPI_API_KEY")
}
