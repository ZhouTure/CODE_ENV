import datetime
import pymysql
import pandas as pd

last_length = None

def get_time():

    today = datetime.date.today()
    # 设置未来的日期
    future_date = datetime.date(2025, 9, 30)
    # 计算两个日期之间的差值
    delta = future_date - today
    return delta.days

def get_mysql():
    # 配置数据库连接参数
    config = {
        # 'host': 'localhost',
        'host': 'host.docker.internal',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'database': 'sales_information',
    }
    db = pymysql.connect(**config)

    try:
        # 创建游标对象
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM table_930 WHERE DATE(create_time) = CURDATE();')
            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            result = cursor.fetchall()
            # 勾到dataframe
            df = pd.DataFrame(result, columns = columns)
            df = df.iloc[:, 2:]
            df.iloc[:, 2:-1] = df.iloc[:, 2:-1].astype(float)
            return df
    finally:
        db.close()


def watch_mysql():
    global last_length
    current_length = 1
    pass


if __name__ == '__main__':
    days = get_time()
    data = get_mysql()
    # 打印结果
    print(f"距离2025年9月30日还有 {days} 天。")
    print(data.info())
    print(data.head(5))
