from settings import REFERRAL_COUNT_FOR_COMMON_RATING
from setup_bot import bot


async def get_user(user_id: int):
    user = await bot.users_api_client.get_user(user_id=user_id)
    return {} if user.get("detail") else user


async def register_new_user(user_id: int, chat_id: int, username: str, first_name: str, last_name: str):
    await bot.users_api_client.create_user(user_id, chat_id, username, first_name, last_name)


async def is_deleted_user(user_id: int):
    user = await bot.users_api_client.get_deleted_user(user_id)
    return False if user.get("detail") else True


async def get_deleted_user(user_id: int):
    return await bot.users_api_client.get_deleted_user(user_id)


async def recreate_user(user_id: int):
    await bot.users_api_client.recreate_user(user_id)


async def update_accept_rules(user_id: int):
    await bot.users_api_client.update_accept_rules(user_id)


async def update_referral_link(user_id: int, referral_link: str):
    await bot.users_api_client.update_referral_link(user_id, referral_link)


async def delete_user(user_id: int):
    await bot.users_api_client.delete_user(user_id)


async def update_common_rating_referral(referral_link: str, rating_value: str = REFERRAL_COUNT_FOR_COMMON_RATING):
    return await bot.users_api_client.update_common_rating_referral(referral_link, rating_value)


async def send_rating_to_user(from_user: int, to_user: int, amount: int):
    return await bot.users_api_client.send_rating_to_other_user(from_user, to_user, amount)


async def get_user_by_referral_link(referral_link: str):
    return await bot.users_api_client.get_user_by_referral_link(referral_link)
