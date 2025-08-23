import time
from numpy import shape
from sqlalchemy import create_engine, inspect, true
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DATETIME, Float, text
import pandas as pd
import datetime
import os
import logging

def mysql_insert(information_dt):
    """
    写入数据库（按位置匹配列）
    :param information_dt: 需要插入的数据（DataFrame）
    :return:
    """
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
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()

    class SalesFirst(Base):
        __tablename__ = 'table_930'
        id = Column(Integer, primary_key=True, autoincrement=True)
        create_time = Column(DATETIME) 
        team = Column(String(10)) 
        name = Column(String(10)) 
        money = Column(Float)
        Sign = Column(String(255))
        
    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("TRUNCATE TABLE table_930"))
                # 反射表结构，获取非自增字段列表
                inspector = inspect(engine)
                columns = inspector.get_columns('table_930')
                non_autoinc_cols = [
                    col["name"] for col in columns
                    if not col.get("autoincrement", False)
                ]
                
                # 检查列数是否一致
                if len(information_dt.columns) != len(non_autoinc_cols):
                    raise ValueError(
                        f"数据列数 ({len(information_dt.columns)}) 与数据库表列数 ({len(non_autoinc_cols)}) 不匹配"
                    )
                
                # 数据处理
                data = [
                    SalesFirst(**dict(zip(non_autoinc_cols, row)))
                    for row in information_dt.values.tolist()
                ]

                session.bulk_save_objects(data)
                session.commit()
                print("数据插入成功。")

    except Exception as e:
        session.rollback()
        print("插入失败:", e)
    finally:
        session.close()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# 卷挂载文件夹
CONTAINER_BASE_PATH = '/data'

today = datetime.date.today()
date_folder = f"{today.year}_{today.month}_{today.day}"
file_name = '2月份表.xlsx'

address = os.path.join(CONTAINER_BASE_PATH, date_folder, file_name)

logging.info(f"尝试在容器内读取文件:{address}")

sheet='930到单'
column_orign = 0

try:
    while True:
        data = pd.read_excel(address, sheet_name = sheet)
        # print("成功读取文件！")
        logging.info('成功读取文件！')
        if column_orign != data.shape[0]:
            column_orign = data.shape[0]
            mysql_insert(data)
        time.sleep(60)
        
except FileNotFoundError:
    logging.info(f"错误：文件未找到！请检查以下几点：")
    logging.info(f"1. 卷挂载是否正确？宿主机的 'E:\\work_file\\data' 是否映射到了容器的 '{CONTAINER_BASE_PATH}'？")
    logging.info(f"2. 在宿主机的 'E:\\work_file\\data' 目录下，是否存在名为 '{date_folder}' 的子文件夹？")
    logging.info(f"3. 在 '{date_folder}' 文件夹下，是否存在名为 '{file_name}' 的文件？")
except Exception as e:
    logging.info(f"发生未知错误{e}")