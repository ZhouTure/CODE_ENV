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

def scheduled_task():
    """
    这是一个包装任务，它会检查当前时间是否在允许的范围内。
    """
    
    # 主题函数
    sign_list = ['🔥', '⚡️', '💥', '🚀']
    count_time = get_time()
    now_time = datetime.now(beijing_tz)
    data = get_mysql()

    # 生成Markdown战报行
    markdown_lines = []
    for i, row in data.iterrows():
        random_icon = random.choice(sign_list)
        line = f"> ▌第{i+1}位 ➤ <font color=\"warning\">**`{row['team']}{row['name']}`**</font> {random_icon} <font color=\"warning\">**`{row['money']:,}`**</font> <font color=\"warning\">**`{row['Sign']}`**</font>"
        markdown_lines.append(line)

    final_markdown_lines = '\n'.join(markdown_lines)

    battle_report = {
        "msgtype": "markdown",
        "markdown": {
            "content": dedent(f"""
    # 🔥【战报速递·倒计时{count_time}天】🔥  
<font color="warning">**起跑即冲刺，开局即决战！勇者无敌，所向披靡！**</font>  
    ### 🚀 {now_time.month}月{now_time.day}日战绩速览  
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
    # 上午: 8, 9, 10, 11 (因为12:00是结束时间，所以11:30是最后一次)
    # 下午: 13, 14, 15, 16, 17, 18, 19 (因为20:00是结束时间，所以19:30是最后一次)
    is_in_morning_window = (8 < current_hour <= 12)
    is_in_afternoon_window = (13 < current_hour <= 20)
    
    if is_in_morning_window or is_in_afternoon_window:
        logging.info(f"[{now_time.strftime('%H:%M')}] 时间符合，准备执行函数。")
        wechat_sent(battle_report)
    else:
        logging.info(f"[{now_time.strftime('%H:%M')}] 当前时间不在预设范围内，本次跳过。")


# scheduled_task()

# 设置定时
schedule.every().hour.at(":00").do(scheduled_task)
# schedule.every().minute.at(":00").do(scheduled_task)
schedule.every().hour.at(":30").do(scheduled_task) 

# 循环
try:
    while True:
        logging.info("Local time is : %s", datetime.now(beijing_tz))
        schedule.run_pending()  # 检查并运行所有待处理的任务
        time.sleep(30)           # 每30秒检查一次
except KeyboardInterrupt:
    logging.error("程序被手动中断。")
