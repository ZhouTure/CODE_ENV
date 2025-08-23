import datetime
from sqlalchemy import create_engine, Column, Integer, DATETIME, String, Float, func
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd

last_length = None

def get_time():
    # 获取今天的日期
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
    db_url = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    engine = create_engine(db_url)
    Session = sessionmaker(bind = engine)
    session = Session()

    Base = declarative_base()
    class Table_930(Base):
        __tablename__ = 'table_930'
        id = Column(Integer, primary_key = True, autoincrement = True)
        create_time = Column(DATETIME)
        team = Column(String(10))
        name = Column(String(10))
        money = Column(Float)
        # Sign = Column(String(255))
        order =  Column(Float)
    
    query = session.query(Table_930).filter(
        func.date(Table_930.create_time) == func.current_date()
    )

    try:
        df = pd.read_sql(query.statement, session.bind)
        df = df.fillna(0)
        result = df.iloc[:, 2:]
        result = result.groupby('name').agg({
            'team': 'first',  # 取每个姓名的第一个战队值
            'money': 'sum',    # 对金额求和
            'order': 'sum'     # 对单数求和
        }).reset_index()

        # # 重新排列列的顺序
        result.sort_values('money', ascending = False, inplace = True)
        result.reset_index(inplace = True)
        result = result[['team', 'name', 'money', 'order']]
        return result
    except Exception as e:
        print(f"失败!错误的原因是:{e}")
