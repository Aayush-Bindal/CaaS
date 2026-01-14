from environs import env

from src.check import check
from src.fetch import get_html
from src.notify import send_telegram_msg
from src.parse import make_sense

print("----------START----------")
env.read_env()
html = get_html()
row_num, hashed_cg, msg_list = make_sense(html)
for i in range(0, row_num):
   print(msg_list[i])
ans = check(row_num, hashed_cg)
if ans:
   print("notifying!!!")
   send_telegram_msg(msg_list)

print("-----------END-----------")