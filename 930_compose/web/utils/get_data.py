import datetime
import pandas as pd
import requests

def get_time():
    # 获取今天的日期
    today = datetime.date.today()

    # 设置未来的日期
    future_date = datetime.date(2025, 9, 30)

    # 计算两个日期之间的差值
    delta = future_date - today
    return delta.days

def get_data():
    url = 'http://localhost:1689/api/records/department/KA'
    
    try:
        response = requests.get(url)
        data = response.json()

        if not data['success']:
            print(f"API返回错误:{data['error']}")
            return
        
        records = data['data']
        print(f"共获取{len(records)}条KA部门记录")
        result = pd.DataFrame(records)
        result['ali_tp_performance'] = result['ali_tp_performance'].astype(float)
        result = result.groupby([
            'department',
            'employee_name'
        ]).agg({
            'ali_tp_performance' : 'sum'
            }).reset_index()
        return result

    except Exception as e:
        print(f"处理数据错误:{e}")
        return None

if __name__ == '__main__':
    data = get_data()
    print(data)
