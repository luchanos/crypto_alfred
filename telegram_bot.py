from aiogram.utils import executor

from handlers import client, join_to_group, send_rating, start, start_for_referrals
from setup_bot import dp


client.register_handlers_client(dp)
start.register_handlers_start(dp)
start_for_referrals.register_handlers_start_for_referrals(dp)
join_to_group.register_handlers_join_to_group(dp)
send_rating.register_handlers_send_rating(dp)


executor.start_polling(dp, skip_updates=True)
