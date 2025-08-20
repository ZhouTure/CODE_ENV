import json
import requests
# import random
# from datetime import datetime
# from data import get_time
# from data import get_mysql
# from textwrap import dedent

def wechat_sent(data):
    url = "your_url"
    headers= {'Content-Type':'application/json'}
    response = requests.post(url,   
                             headers=headers,
                             data=json.dumps(data))
    if response.status_code == 200:
        print('Sent succesd!')
        return None
    else:
        print(f"Error getting access token: {response.status_code}, {response.text}")
        return None


# if __name__ == '__main__':
#     sign_list = ['🔥', '⚡️', '💥', '🚀']
#     count_time = get_time()
#     now_time = datetime.now()
#     data = get_mysql()

#     # 生成Markdown战报行
#     markdown_lines = []
#     for i, row in data.iterrows():
#         random_icon = random.choice(sign_list)
#         line = f"> ▌第{i+1}单 ➤ <font color=\"warning\">**`{row['team']}{row['name']}`**</font> {random_icon} <font color=\"warning\">**`{row['money']:,}`**</font>"
#         markdown_lines.append(line)
    
#     final_markdown_lines = '\n'.join(markdown_lines)

#     battle_report = {
#         "msgtype": "markdown",
#         "markdown": {
#             "content": dedent(f"""
# # 🔥【战报速递·倒计时{count_time}天】🔥  
# <font color="warning">**起跑即冲刺，开局即决战！勇者无敌，所向披靡！**</font>  
# <font color="warning">**勇者无敌，所向披靡！**</font>  
# ### 🚀 {now_time.month}月{now_time.day}日战绩速览  
# <font color="warning">💪💪💪到账接龙💥💥💥</font>  
# 🏆 **今日战神榜** ⚔️  

# {final_markdown_lines} 

# <font color="comment">**谁是下一位英雄？兄弟们，搞起来！**</font>  
# ⚡ <font color="warning">**🚀是不是你？兄弟们！搞起来，此刻不搏更待何时？**</font>  
# 💪 <font color="warning">**全员冲锋，火力全开！**</font>  
# """)
#         }
#     }
#     wechat_sent(battle_report)