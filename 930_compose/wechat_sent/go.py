from re import match
from unittest import case
from utils.wechat import wechat_sent
from utils.data import get_mysql
from utils.data import get_time
from textwrap import dedent
from datetime import datetime
import random
import schedule
import time
import logging
import pytz

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# 获取北京时间
beijing_tz = pytz.timezone('Asia/Shanghai')

def rd_sign(i, list1, list2):
    if i == 0 : return list1[0]
    elif i == 1 : return list1[1]
    elif i == 2 : return list1[2]
    else : return random.choice(list2)

def scheduled_task():
    """
    这是一个包装任务，它会检查当前时间是否在允许的范围内。
    """
    # 主题函数
    sign_list = ['🔥', '⚡️', '💥', '🚀', '🌟']
    count_time = get_time()
    now_time = datetime.now(beijing_tz)
    data = get_mysql()

    # 生成Markdown战报行
    markdown_lines = []
    top_lines = []

    if data is not None:
        for i, row in data.iterrows():
            crow = ['🥇', '🥈', '🥉']
            size = ['25', '20', '15']
            if i<3:
                line3 = f"> <font size={size[i]}> {crow[i]}**{data.iloc[i, 1]}**{crow[i]} </font> "
                top_lines.append(line3)

            line = f"> ▌第{i+1}名 ➤ <font color=\"warning\">**`{row['team']}{row['name']}`**</font>{rd_sign(i, crow, sign_list)}<font color=\"warning\">**合计到账`{row['money']:,}`元，合计到单`{row['order']}`单**</font>"
            markdown_lines.append(line)

    final_markdown_lines = '\n'.join(markdown_lines)
    final_top_lines = '\n'.join(top_lines)

    battle_report = {
        "msgtype": "markdown",
        "markdown": {
            "content": dedent(f"""
    # 🔥【战报速递·倒计时{count_time}天】🔥  
<font color="warning">**起跑即冲刺，开局即决战！勇者无敌，所向披靡！**</font>  
    ### 🚀 {now_time.month}月{now_time.day}日战绩速览

    # **⚔️ 战神风云榜**（实时刷新）：  

    {final_top_lines}

<font color="warning">💪💪💪到账接龙💥💥💥</font>  
🏆 **今日战神榜** ⚔️  

    {final_markdown_lines} 

<font color="comment">**谁是下一位英雄  ？兄弟们，搞起来！**</font>  
⚡ <font color="warning">**🚀是不是你？此刻不搏更待何时？**</font>  
💪 <font color="warning">**全员冲锋，火力全开！**</font>  
    """)
                        }
                    }
    
    current_hour = now_time.hour
    
    # 定义允许执行的小时范围
    is_in_morning_window = (8 < current_hour <= 12)
    is_in_afternoon_window = (13 < current_hour <= 20)
    
    if is_in_morning_window or is_in_afternoon_window:
        logging.info(f"[{now_time.strftime('%H:%M')}] 时间符合，准备执行函数。")
        wechat_sent(battle_report)
    else:
        logging.info(f"[{now_time.strftime('%H:%M')}] 当前时间不在预设范围内，本次跳过。")



# 设置定时
schedule.every().hour.at(":00").do(scheduled_task)
schedule.every().hour.at(":30").do(scheduled_task) 

# 循环
try:
    while True:
        logging.info("Local time is : %s", datetime.now(beijing_tz))
        schedule.run_pending()  # 检查并运行所有待处理的任务
        time.sleep(30)           # 每30秒检查一次
except KeyboardInterrupt:
    logging.error("程序被手动中断。")