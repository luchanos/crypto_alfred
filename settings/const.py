from .base import env


REFERRAL_COUNT_FOR_COMMON_RATING = env.int("REFERRAL_COUNT_FOR_COMMON_RATING", default=10)

DEFAULT_EXCHANGE_RATES = env.list(
    "DEFAULT_EXCHANGE_RATES", default=["BTC", "ETH", "BNB", "ADA", "SOL", "DOT", "XPR"]
)
