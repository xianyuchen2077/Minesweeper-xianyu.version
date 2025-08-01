from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库文件路径
DATABASE = 'leaderboard.db'

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            time INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    """首页"""
    return jsonify({"message": "扫雷排行榜服务器运行中！"})

@app.route('/api/scores', methods=['POST'])
def add_score():
    """添加新成绩"""
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "无效的JSON数据"}), 400

        name = data.get('name', '').strip()
        difficulty = data.get('difficulty', '')
        time_seconds = data.get('time', 0)

        if not name or not difficulty or time_seconds <= 0:
            return jsonify({"error": "无效的数据"}), 400

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('INSERT INTO scores (name, difficulty, time) VALUES (?, ?, ?)',
                (name, difficulty, time_seconds))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "成绩保存成功！"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scores/<difficulty>', methods=['GET'])
def get_scores(difficulty):
    """获取指定难度的排行榜"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            SELECT name, time, created_at
            FROM scores
            WHERE difficulty = ?
            ORDER BY time ASC
            LIMIT 10
        ''', (difficulty,))

        scores = []
        for row in c.fetchall():
            scores.append({
                "name": row[0],
                "time": row[1],
                "created_at": row[2]
            })

        conn.close()
        return jsonify(scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scores', methods=['GET'])
def get_all_scores():
    """获取所有难度的排行榜"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            SELECT difficulty, name, time, created_at
            FROM scores
            ORDER BY difficulty, time ASC
        ''')

        all_scores = {}
        for row in c.fetchall():
            difficulty, name, time_seconds, created_at = row
            if difficulty not in all_scores:
                all_scores[difficulty] = []
            all_scores[difficulty].append({
                "name": name,
                "time": time_seconds,
                "created_at": created_at
            })

        # 每个难度只保留前10名
        for difficulty in all_scores:
            all_scores[difficulty] = all_scores[difficulty][:10]

        conn.close()
        return jsonify(all_scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)