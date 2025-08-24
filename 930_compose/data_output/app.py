from flask import Flask, jsonify
from utils.data_output import DatabaseManage, DatabaseConfig

app = Flask(__name__)

# 初始化数据库管理器
db_config = DatabaseConfig()
db_manager = DatabaseManage(db_config)

@app.route('/api/records/today', methods = ['GET'])
def get_today_records():
    """获取今天记录"""
    try:
        records = db_manager.get_today_records()
        return jsonify({
            'success' : True,
            'data' : records,
            'count' : len(records)
        })
    except Exception as e:
        return jsonify({
            'success' : False,
            'error' : str(e)
        }), 500

@app.route('/api/records/department/KA', methods = ['GET'])
def get_department_records():
    """获取KA部门记录"""
    try:
        records = db_manager.get_department_records()
        return jsonify({
            'success' : True,
            'data' : records,
            'count' : len(records)
        })
    except Exception as e:
        return jsonify({
            'success' : False,
            'error' : str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5000)

