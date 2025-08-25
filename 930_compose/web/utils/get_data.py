import datetime
import requests
import pandas as pd

def get_time():
    # 获取今天的日期
    today = datetime.date.today()

    # 设置未来的日期
    future_date = datetime.date(2025, 9, 30)

    # 计算两个日期之间的差值
    delta = future_date - today
    return delta.days

def get_data():
    "从restful API获取数据"
    url = 'http://data_output:5000/api/records/today'
    try:
        response = requests.get(url)
        data = response.json()

        if not data['success']:
            print(f"API返回错误:{data['error']}")
            return
        
        records = data['data']
        print(f"共获取{len(records)}条今日记录")
        result = pd.DataFrame(records)
        result = result.groupby([
            'team',
            'name'
        ]).agg({
            'money' : 'sum',
            'order' : 'sum'
            }).reset_index()
        result.sort_values('money', ascending = False, inplace = True)
        result = result.reset_index().iloc[:, 1:]
        return result

    except Exception as e:
        print(f"处理数据错误:{e}")
        return None

if __name__ == '__main__':
    days = get_time()
    data = get_data()
    # 打印结果
    print(f"距离2025年9月30日还有 {days} 天。")
    print(data.info())
    print(data.head(5))
