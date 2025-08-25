from sqlalchemy import create_engine, Column, Integer, DATETIME, String, Float, func, DECIMAL
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
import contextlib

class DatabaseConfig:
    """数据库配置"""
    def __init__(self):
        self.config = {
            # 'host': 'localhost',
            'host': 'host.docker.internal',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'sales_information',  
        }

    def get_db_url(self):
        "获取数据连接URL"
        return f"mysql+pymysql://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"

Base = declarative_base()

class Table_930(Base):
        """定义表类"""
        __tablename__ = 'table_930'
        id = Column(Integer, primary_key = True, autoincrement = True)
        create_time = Column(DATETIME)
        team = Column(String(10))
        name = Column(String(10))
        money = Column(Float)
        Sign = Column(String(255))
        order =  Column(Float)

        def to_dict(self):
            "对象转换为字典"
            return {
                'id': self.id,
                'create_time': self.create_time.isoformat() if self.create_time else None,
                'team': self.team,
                'name': self.name,
                'money': self.money,
                'order': self.order
            }

class DatabaseManage:
    def __init__(self, db_config : DatabaseConfig):
        self.db_config = db_config
        self.engine = create_engine(self.db_config.get_db_url())
        self.Session = sessionmaker(bind = self.engine)

    @contextlib.contextmanager
    def get_session(self):
        """获取数据库会话的上下文管理器"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_today_records(self):
        """获取今天的记录"""
        with self.get_session() as session:
            query = session.query(Table_930).filter(
                func.date(Table_930.create_time) == func.current_date()
            ).all()
            return [record.to_dict() for record in query]
    
    def get_department_records(self):
        """获取特定部门的记录"""
        with self.get_session() as session:
            query = session.query(Table_930).filter(
                Table_930.department == 'KA'
            ).all()
            return [record.to_dict() for record in query]
    
    

    
         
