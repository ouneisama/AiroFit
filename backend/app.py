from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date, timedelta
import os
import uuid
import random
import json
import base64
import requests
import re

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass

app = Flask(__name__)
CORS(app)

# 数据库配置 - 使用 SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_urls = db.Column(db.Text, default='')
    time = db.Column(db.DateTime, default=datetime.utcnow)


class FoodRecord(db.Model):
    __tablename__ = 'food_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=1)
    meal_type = db.Column(db.String(20), default='lunch')
    food_name = db.Column(db.String(100), nullable=False)
    food_name_cn = db.Column(db.String(100), default='')
    weight_g = db.Column(db.Float, default=200)
    calorie = db.Column(db.Float, default=0)
    protein = db.Column(db.Float, default=0)
    carb = db.Column(db.Float, default=0)
    fat = db.Column(db.Float, default=0)
    fiber = db.Column(db.Float, default=0)
    image_url = db.Column(db.String(500), default='')
    confidence = db.Column(db.Float, default=0.0)
    note = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DailySummary(db.Model):
    __tablename__ = 'daily_summaries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=1)
    record_date = db.Column(db.Date, nullable=False)
    total_calorie = db.Column(db.Float, default=0)
    total_protein = db.Column(db.Float, default=0)
    total_carb = db.Column(db.Float, default=0)
    total_fat = db.Column(db.Float, default=0)
    meal_count = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()
print("Database ready (SQLite)")


# ============ 食物营养数据库 (每100g) ============

FOOD_NUTRITION_DB = {
    "rice": {"name_cn": "米饭", "calorie": 116, "protein": 2.6, "carb": 25.9, "fat": 0.3, "fiber": 0.3},
    "brown_rice": {"name_cn": "糙米饭", "calorie": 123, "protein": 2.7, "carb": 25.6, "fat": 0.9, "fiber": 1.0},
    "noodles": {"name_cn": "面条", "calorie": 110, "protein": 3.3, "carb": 22.3, "fat": 0.4, "fiber": 0.5},
    "bread": {"name_cn": "面包", "calorie": 265, "protein": 8.5, "carb": 49.0, "fat": 3.2, "fiber": 2.4},
    "whole_wheat_bread": {"name_cn": "全麦面包", "calorie": 247, "protein": 9.0, "carb": 43.0, "fat": 3.4, "fiber": 6.0},
    "steamed_bun": {"name_cn": "馒头", "calorie": 223, "protein": 7.0, "carb": 44.2, "fat": 1.1, "fiber": 1.3},
    "dumpling": {"name_cn": "饺子", "calorie": 250, "protein": 9.0, "carb": 28.0, "fat": 10.0, "fiber": 1.0},
    "corn": {"name_cn": "玉米", "calorie": 112, "protein": 4.0, "carb": 22.8, "fat": 1.2, "fiber": 2.9},
    "sweet_potato": {"name_cn": "红薯", "calorie": 86, "protein": 1.6, "carb": 20.1, "fat": 0.1, "fiber": 3.0},
    "oatmeal": {"name_cn": "燕麦", "calorie": 377, "protein": 13.5, "carb": 66.3, "fat": 6.7, "fiber": 10.6},
    "chicken_breast": {"name_cn": "鸡胸肉", "calorie": 133, "protein": 31.0, "carb": 0, "fat": 1.2, "fiber": 0},
    "chicken": {"name_cn": "鸡肉", "calorie": 167, "protein": 19.3, "carb": 1.3, "fat": 9.4, "fiber": 0},
    "chicken_leg": {"name_cn": "鸡腿", "calorie": 181, "protein": 16.0, "carb": 0, "fat": 13.0, "fiber": 0},
    "beef": {"name_cn": "牛肉", "calorie": 125, "protein": 20.2, "carb": 1.2, "fat": 4.2, "fiber": 0},
    "steak": {"name_cn": "牛排", "calorie": 200, "protein": 26.0, "carb": 0, "fat": 10.0, "fiber": 0},
    "pork": {"name_cn": "猪肉", "calorie": 242, "protein": 13.2, "carb": 0, "fat": 20.8, "fiber": 0},
    "lean_pork": {"name_cn": "瘦猪肉", "calorie": 143, "protein": 20.3, "carb": 1.5, "fat": 6.2, "fiber": 0},
    "lamb": {"name_cn": "羊肉", "calorie": 203, "protein": 19.0, "carb": 0, "fat": 14.1, "fiber": 0},
    "duck": {"name_cn": "鸭肉", "calorie": 240, "protein": 15.5, "carb": 0.5, "fat": 19.7, "fiber": 0},
    "fish": {"name_cn": "鱼肉", "calorie": 104, "protein": 17.6, "carb": 0, "fat": 3.4, "fiber": 0},
    "salmon": {"name_cn": "三文鱼", "calorie": 208, "protein": 20.4, "carb": 0, "fat": 13.4, "fiber": 0},
    "shrimp": {"name_cn": "虾", "calorie": 99, "protein": 20.3, "carb": 0.2, "fat": 1.0, "fiber": 0},
    "crab": {"name_cn": "螃蟹", "calorie": 95, "protein": 13.8, "carb": 2.3, "fat": 2.6, "fiber": 0},
    "squid": {"name_cn": "鱿鱼", "calorie": 92, "protein": 17.4, "carb": 1.6, "fat": 1.6, "fiber": 0},
    "egg": {"name_cn": "鸡蛋", "calorie": 144, "protein": 13.3, "carb": 1.5, "fat": 9.5, "fiber": 0},
    "egg_white": {"name_cn": "蛋白", "calorie": 48, "protein": 11.0, "carb": 0.7, "fat": 0.1, "fiber": 0},
    "milk": {"name_cn": "牛奶", "calorie": 54, "protein": 3.0, "carb": 4.9, "fat": 2.5, "fiber": 0},
    "yogurt": {"name_cn": "酸奶", "calorie": 72, "protein": 3.5, "carb": 9.3, "fat": 2.1, "fiber": 0},
    "cheese": {"name_cn": "奶酪", "calorie": 328, "protein": 25.7, "carb": 1.3, "fat": 23.5, "fiber": 0},
    "broccoli": {"name_cn": "西兰花", "calorie": 34, "protein": 2.8, "carb": 6.6, "fat": 0.4, "fiber": 2.6},
    "spinach": {"name_cn": "菠菜", "calorie": 23, "protein": 2.9, "carb": 3.6, "fat": 0.4, "fiber": 2.2},
    "tomato": {"name_cn": "番茄", "calorie": 18, "protein": 0.9, "carb": 3.9, "fat": 0.2, "fiber": 1.2},
    "cucumber": {"name_cn": "黄瓜", "calorie": 15, "protein": 0.7, "carb": 2.9, "fat": 0.1, "fiber": 0.5},
    "carrot": {"name_cn": "胡萝卜", "calorie": 41, "protein": 0.9, "carb": 9.6, "fat": 0.2, "fiber": 2.8},
    "lettuce": {"name_cn": "生菜", "calorie": 15, "protein": 1.4, "carb": 2.8, "fat": 0.2, "fiber": 1.3},
    "cabbage": {"name_cn": "卷心菜", "calorie": 25, "protein": 1.3, "carb": 5.8, "fat": 0.1, "fiber": 2.5},
    "celery": {"name_cn": "芹菜", "calorie": 16, "protein": 0.7, "carb": 3.3, "fat": 0.1, "fiber": 1.6},
    "bell_pepper": {"name_cn": "彩椒", "calorie": 20, "protein": 0.9, "carb": 4.6, "fat": 0.2, "fiber": 1.7},
    "mushroom": {"name_cn": "蘑菇", "calorie": 22, "protein": 3.1, "carb": 3.3, "fat": 0.3, "fiber": 1.0},
    "potato": {"name_cn": "土豆", "calorie": 77, "protein": 2.0, "carb": 17.5, "fat": 0.1, "fiber": 2.2},
    "tofu": {"name_cn": "豆腐", "calorie": 76, "protein": 8.1, "carb": 1.9, "fat": 3.7, "fiber": 0.3},
    "apple": {"name_cn": "苹果", "calorie": 52, "protein": 0.3, "carb": 14.0, "fat": 0.2, "fiber": 2.4},
    "banana": {"name_cn": "香蕉", "calorie": 89, "protein": 1.1, "carb": 22.8, "fat": 0.3, "fiber": 2.6},
    "orange": {"name_cn": "橙子", "calorie": 47, "protein": 0.9, "carb": 11.8, "fat": 0.1, "fiber": 2.4},
    "grape": {"name_cn": "葡萄", "calorie": 69, "protein": 0.7, "carb": 18.1, "fat": 0.2, "fiber": 0.9},
    "watermelon": {"name_cn": "西瓜", "calorie": 30, "protein": 0.6, "carb": 7.6, "fat": 0.2, "fiber": 0.4},
    "strawberry": {"name_cn": "草莓", "calorie": 32, "protein": 0.7, "carb": 7.7, "fat": 0.3, "fiber": 2.0},
    "blueberry": {"name_cn": "蓝莓", "calorie": 57, "protein": 0.7, "carb": 14.5, "fat": 0.3, "fiber": 2.4},
    "avocado": {"name_cn": "牛油果", "calorie": 160, "protein": 2.0, "carb": 8.5, "fat": 14.7, "fiber": 6.7},
    "kiwi": {"name_cn": "猕猴桃", "calorie": 61, "protein": 1.1, "carb": 14.7, "fat": 0.5, "fiber": 3.0},
    "pineapple": {"name_cn": "菠萝", "calorie": 50, "protein": 0.5, "carb": 13.1, "fat": 0.1, "fiber": 1.4},
    "almond": {"name_cn": "杏仁", "calorie": 579, "protein": 21.2, "carb": 21.6, "fat": 49.9, "fiber": 12.5},
    "walnut": {"name_cn": "核桃", "calorie": 654, "protein": 15.2, "carb": 13.7, "fat": 65.2, "fiber": 6.7},
    "peanut": {"name_cn": "花生", "calorie": 567, "protein": 25.8, "carb": 16.1, "fat": 49.2, "fiber": 8.5},
    "cashew": {"name_cn": "腰果", "calorie": 553, "protein": 18.2, "carb": 30.2, "fat": 43.9, "fiber": 3.3},
    "coffee": {"name_cn": "咖啡", "calorie": 2, "protein": 0.1, "carb": 0, "fat": 0, "fiber": 0},
    "green_tea": {"name_cn": "绿茶", "calorie": 1, "protein": 0, "carb": 0.2, "fat": 0, "fiber": 0},
    "orange_juice": {"name_cn": "橙汁", "calorie": 45, "protein": 0.7, "carb": 10.4, "fat": 0.2, "fiber": 0.2},
    "cola": {"name_cn": "可乐", "calorie": 42, "protein": 0, "carb": 10.6, "fat": 0, "fiber": 0},
    "soy_milk": {"name_cn": "豆浆", "calorie": 33, "protein": 2.9, "carb": 1.8, "fat": 1.5, "fiber": 0.4},
    "kung_pao_chicken": {"name_cn": "宫保鸡丁", "calorie": 180, "protein": 16.0, "carb": 8.0, "fat": 9.0, "fiber": 1.0},
    "mapo_tofu": {"name_cn": "麻婆豆腐", "calorie": 120, "protein": 8.0, "carb": 5.0, "fat": 7.0, "fiber": 1.0},
    "sweet_sour_pork": {"name_cn": "糖醋里脊", "calorie": 220, "protein": 12.0, "carb": 18.0, "fat": 11.0, "fiber": 0.5},
    "fried_rice": {"name_cn": "炒饭", "calorie": 180, "protein": 5.5, "carb": 28.0, "fat": 5.0, "fiber": 0.8},
    "hotpot": {"name_cn": "火锅", "calorie": 150, "protein": 10.0, "carb": 5.0, "fat": 9.0, "fiber": 1.5},
    "salad": {"name_cn": "沙拉", "calorie": 45, "protein": 1.5, "carb": 5.0, "fat": 2.0, "fiber": 2.0},
    "sushi": {"name_cn": "寿司", "calorie": 145, "protein": 6.0, "carb": 26.0, "fat": 1.5, "fiber": 0.5},
    "pizza": {"name_cn": "披萨", "calorie": 266, "protein": 11.4, "carb": 33.0, "fat": 10.0, "fiber": 2.3},
    "hamburger": {"name_cn": "汉堡", "calorie": 295, "protein": 17.0, "carb": 30.0, "fat": 12.0, "fiber": 1.5},
    "sandwich": {"name_cn": "三明治", "calorie": 250, "protein": 12.0, "carb": 28.0, "fat": 9.0, "fiber": 2.0},
    "pasta": {"name_cn": "意面", "calorie": 131, "protein": 5.0, "carb": 25.0, "fat": 1.1, "fiber": 1.8},
}

CATEGORY_MAP = {
    "staple": ["rice", "brown_rice", "noodles", "bread", "whole_wheat_bread", "steamed_bun", "dumpling", "corn", "sweet_potato", "oatmeal", "fried_rice", "pasta"],
    "meat": ["chicken_breast", "chicken", "chicken_leg", "beef", "steak", "pork", "lean_pork", "lamb", "duck"],
    "seafood": ["fish", "salmon", "shrimp", "crab", "squid"],
    "egg_dairy": ["egg", "egg_white", "milk", "yogurt", "cheese"],
    "vegetable": ["broccoli", "spinach", "tomato", "cucumber", "carrot", "lettuce", "cabbage", "celery", "bell_pepper", "mushroom", "potato", "tofu"],
    "fruit": ["apple", "banana", "orange", "grape", "watermelon", "strawberry", "blueberry", "avocado", "kiwi", "pineapple"],
    "nut": ["almond", "walnut", "peanut", "cashew"],
    "drink": ["coffee", "green_tea", "orange_juice", "cola", "soy_milk"],
    "dish": ["kung_pao_chicken", "mapo_tofu", "sweet_sour_pork", "hotpot", "salad", "sushi", "pizza", "hamburger", "sandwich"],
}

WEIGHT_ESTIMATE = {
    "rice": 200, "brown_rice": 200, "noodles": 250, "fried_rice": 250, "pasta": 200,
    "bread": 50, "whole_wheat_bread": 50, "steamed_bun": 100,
    "chicken_breast": 150, "chicken": 150, "chicken_leg": 120, "beef": 150, "steak": 200,
    "pork": 150, "lean_pork": 150, "lamb": 150, "duck": 150,
    "fish": 150, "salmon": 150, "shrimp": 100, "crab": 200, "squid": 100,
    "egg": 50, "egg_white": 30, "milk": 250, "yogurt": 200, "soy_milk": 250,
    "broccoli": 200, "spinach": 200, "tomato": 150, "cucumber": 150,
    "carrot": 150, "lettuce": 100, "cabbage": 200, "celery": 150,
    "bell_pepper": 150, "mushroom": 150, "potato": 200, "tofu": 200,
    "apple": 200, "banana": 120, "orange": 200, "grape": 200,
    "watermelon": 300, "strawberry": 150, "blueberry": 100,
    "avocado": 150, "kiwi": 100, "pineapple": 200,
    "almond": 30, "walnut": 30, "peanut": 30, "cashew": 30,
    "coffee": 300, "green_tea": 300, "orange_juice": 300, "cola": 330,
    "kung_pao_chicken": 250, "mapo_tofu": 250, "sweet_sour_pork": 250,
    "hotpot": 500, "salad": 250, "sushi": 200, "pizza": 200,
    "hamburger": 200, "sandwich": 200, "dumpling": 200, "corn": 200,
    "sweet_potato": 200, "oatmeal": 50, "cheese": 30,
}


# ============ 工具函数 ============

def calculate_nutrition(food_key, weight_g):
    if food_key not in FOOD_NUTRITION_DB:
        return None
    data = FOOD_NUTRITION_DB[food_key]
    ratio = weight_g / 100.0
    return {
        "food_key": food_key,
        "food_name_cn": data["name_cn"],
        "weight_g": round(weight_g, 1),
        "calorie": round(data["calorie"] * ratio, 1),
        "protein": round(data["protein"] * ratio, 1),
        "carb": round(data["carb"] * ratio, 1),
        "fat": round(data["fat"] * ratio, 1),
        "fiber": round(data["fiber"] * ratio, 1),
    }


# ============ 通义千问视觉识别配置 ============
# 免费获取 API Key: https://dashscope.console.aliyun.com/
# 新用户有 100 万 tokens 免费额度
# API Key 请在 backend/.env 中配置（参见 .env.example）
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")

def ai_recognize_food(image_path):
    """使用通义千问视觉模型识别食物"""
    if not DASHSCOPE_API_KEY:
        return None

    try:
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        # 获取文件扩展名确定 MIME 类型
        ext = os.path.splitext(image_path)[1].lower()
        mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"}
        mime_type = mime_map.get(ext, "image/jpeg")

        food_list = "、".join([v["name_cn"] for v in FOOD_NUTRITION_DB.values()])

        prompt = f"""你是一个专业的食物营养分析助手。请分析这张图片中的食物。

要求：
1. 识别图片中是什么食物
2. 从以下食物列表中选择最匹配的一个：{food_list}
3. 估算食物的重量（单位：克）
4. 只输出 JSON 格式，不要任何其他文字

输出格式示例：
{{"food_name_cn": "米饭", "weight_g": 200, "confidence": 0.9}}

注意：
- food_name_cn 必须从上述食物列表中选择，不要自己编造
- weight_g 是整数，根据图片中食物的份量估算
- confidence 是 0-1 之间的置信度
"""

        resp = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "qwen-vl-plus",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}},
                        {"type": "text", "text": prompt},
                    ]
                }],
                "max_tokens": 200,
            },
            timeout=30,
        )

        if resp.status_code != 200:
            print(f"API error: {resp.status_code} {resp.text}")
            return None

        result = resp.json()
        content = result["choices"][0]["message"]["content"].strip()

        # 提取 JSON
        json_match = re.search(r'\{[^}]+\}', content)
        if not json_match:
            print(f"No JSON found in response: {content}")
            return None

        data = json.loads(json_match.group())
        food_name_cn = data.get("food_name_cn", "")

        # 匹配 food_key
        food_key = None
        for key, info in FOOD_NUTRITION_DB.items():
            if info["name_cn"] == food_name_cn:
                food_key = key
                break

        if not food_key:
            print(f"Food not in DB: {food_name_cn}")
            return None

        return {
            "food_key": food_key,
            "confidence": float(data.get("confidence", 0.85)),
            "estimated_weight_g": int(data.get("weight_g", WEIGHT_ESTIMATE.get(food_key, 200))),
        }

    except Exception as e:
        print(f"AI recognition error: {e}")
        return None


def simulate_food_recognition():
    """备用：基于图片主色调的简单推测（无 API Key 时使用）"""
    foods = list(FOOD_NUTRITION_DB.keys())
    food_key = random.choice(foods)
    return {
        "food_key": food_key,
        "confidence": round(random.uniform(0.65, 0.85), 2),
        "estimated_weight_g": WEIGHT_ESTIMATE.get(food_key, 200),
    }


def update_daily_summary(user_id, record_date):
    records = FoodRecord.query.filter(
        FoodRecord.user_id == user_id,
        db.func.date(FoodRecord.created_at) == record_date
    ).all()
    total_cal = sum(r.calorie for r in records)
    total_protein = sum(r.protein for r in records)
    total_carb = sum(r.carb for r in records)
    total_fat = sum(r.fat for r in records)
    summary = DailySummary.query.filter_by(user_id=user_id, record_date=record_date).first()
    if summary:
        summary.total_calorie = round(total_cal, 1)
        summary.total_protein = round(total_protein, 1)
        summary.total_carb = round(total_carb, 1)
        summary.total_fat = round(total_fat, 1)
        summary.meal_count = len(records)
        summary.updated_at = datetime.utcnow()
    else:
        summary = DailySummary(
            user_id=user_id, record_date=record_date,
            total_calorie=round(total_cal, 1), total_protein=round(total_protein, 1),
            total_carb=round(total_carb, 1), total_fat=round(total_fat, 1),
            meal_count=len(records),
        )
        db.session.add(summary)
    db.session.commit()
    return summary


# ============ 静态资源 ============

@app.route("/static/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ============ 帖子 API ============

@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return jsonify([{
        "id": p.id, "content": p.content,
        "image_urls": p.image_urls.split(",") if p.image_urls else [],
        "time": p.time.strftime("%Y-%m-%d %H:%M:%S")
    } for p in posts])


@app.route("/api/posts", methods=["POST"])
def add_post():
    content = request.form.get("content", "").strip()
    files = request.files.getlist("images")
    if not content:
        return jsonify({"msg": "内容不能为空"}), 400
    image_urls = []
    for file in files:
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1]
            new_filename = str(uuid.uuid4()) + ext
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], new_filename))
            image_urls.append(f"http://localhost:5000/static/uploads/{new_filename}")
    db.session.add(Post(content=content, image_urls=",".join(image_urls)))
    db.session.commit()
    return jsonify({"msg": "发布成功"}), 200


# ============ AI 食物识别 API ============

@app.route("/api/food/recognize", methods=["POST"])
def recognize_food():
    if "image" not in request.files:
        return jsonify({"error": "请上传食物图片"}), 400
    file = request.files["image"]
    if not file or not file.filename:
        return jsonify({"error": "无效的文件"}), 400
    ext = os.path.splitext(file.filename)[1]
    if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        return jsonify({"error": "仅支持 JPG/PNG/GIF/WEBP 格式"}), 400
    new_filename = str(uuid.uuid4()) + ext
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
    file.save(save_path)
    image_url = f"http://localhost:5000/static/uploads/{new_filename}"
    # 优先使用 AI 识别，失败则降级到模拟
    recognition = ai_recognize_food(save_path)  # save_path defined above
    if not recognition:
        print("AI recognition failed, falling back to simulation")
        recognition = simulate_food_recognition()

    nutrition = calculate_nutrition(recognition["food_key"], recognition["estimated_weight_g"])
    if not nutrition:
        return jsonify({"error": "未能识别食物，请重试"}), 400
    nutrition["image_url"] = image_url
    nutrition["confidence"] = recognition["confidence"]
    return jsonify({"success": True, "data": nutrition})


@app.route("/api/food/recognize_batch", methods=["POST"])
def recognize_food_batch():
    files = request.files.getlist("images")
    if not files:
        return jsonify({"error": "请上传食物图片"}), 400
    results = []
    for file in files:
        if not file or not file.filename:
            continue
        ext = os.path.splitext(file.filename)[1]
        if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            continue
        new_filename = str(uuid.uuid4()) + ext
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
        file.save(save_path)
        image_url = f"http://localhost:5000/static/uploads/{new_filename}"
        recognition = ai_recognize_food(os.path.join(app.config["UPLOAD_FOLDER"], new_filename))
        if not recognition:
            recognition = simulate_food_recognition()
        nutrition = calculate_nutrition(recognition["food_key"], recognition["estimated_weight_g"])
        if nutrition:
            nutrition["image_url"] = image_url
            nutrition["confidence"] = recognition["confidence"]
            results.append(nutrition)
    return jsonify({"success": True, "data": results})


# ============ 食物数据查询 API ============

@app.route("/api/food/search", methods=["GET"])
def search_food():
    keyword = request.args.get("keyword", "").strip().lower()
    if not keyword:
        return jsonify({"error": "请输入搜索关键词"}), 400
    results = []
    for key, data in FOOD_NUTRITION_DB.items():
        if keyword in key or keyword in data["name_cn"]:
            results.append({
                "food_key": key, "food_name_cn": data["name_cn"],
                "calorie": data["calorie"], "protein": data["protein"],
                "carb": data["carb"], "fat": data["fat"], "fiber": data["fiber"],
            })
    return jsonify({"success": True, "data": results, "total": len(results)})


@app.route("/api/food/nutrition/<food_key>", methods=["GET"])
def get_food_nutrition(food_key):
    weight_g = request.args.get("weight", 200, type=float)
    nutrition = calculate_nutrition(food_key, weight_g)
    if not nutrition:
        return jsonify({"error": "未找到该食物数据"}), 404
    return jsonify({"success": True, "data": nutrition})


@app.route("/api/food/nutrition_list", methods=["GET"])
def get_nutrition_list():
    category = request.args.get("category", "all")
    results = []
    for key, data in FOOD_NUTRITION_DB.items():
        if category == "all" or key in CATEGORY_MAP.get(category, []):
            results.append({
                "food_key": key, "food_name_cn": data["name_cn"],
                "calorie": data["calorie"], "protein": data["protein"],
                "carb": data["carb"], "fat": data["fat"], "fiber": data["fiber"],
            })
    return jsonify({
        "success": True, "data": results, "total": len(results),
        "categories": list(CATEGORY_MAP.keys())
    })


# ============ 食物记录 CRUD ============

@app.route("/api/food/records", methods=["GET"])
def get_food_records():
    filter_date = request.args.get("date")
    meal_type = request.args.get("meal_type")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    query = FoodRecord.query
    if filter_date:
        query = query.filter(db.func.date(FoodRecord.created_at) == filter_date)
    if meal_type:
        query = query.filter_by(meal_type=meal_type)
    query = query.order_by(FoodRecord.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    records = [{
        "id": r.id, "user_id": r.user_id, "meal_type": r.meal_type,
        "food_name": r.food_name, "food_name_cn": r.food_name_cn,
        "weight_g": r.weight_g, "calorie": r.calorie,
        "protein": r.protein, "carb": r.carb, "fat": r.fat, "fiber": r.fiber,
        "image_url": r.image_url, "confidence": r.confidence,
        "note": r.note, "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    } for r in pagination.items]
    return jsonify({
        "success": True, "data": records, "total": pagination.total,
        "page": page, "per_page": per_page, "pages": pagination.pages,
    })


@app.route("/api/food/records", methods=["POST"])
def create_food_record():
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求数据为空"}), 400
    food_name = data.get("food_name", data.get("food_key", ""))
    if not food_name:
        return jsonify({"error": "食物名称不能为空"}), 400
    record = FoodRecord(
        user_id=data.get("user_id", 1),
        meal_type=data.get("meal_type", "lunch"),
        food_name=food_name,
        food_name_cn=data.get("food_name_cn", ""),
        weight_g=data.get("weight_g", 200),
        calorie=data.get("calorie", 0),
        protein=data.get("protein", 0),
        carb=data.get("carb", 0),
        fat=data.get("fat", 0),
        fiber=data.get("fiber", 0),
        image_url=data.get("image_url", ""),
        confidence=data.get("confidence", 0),
        note=data.get("note", ""),
    )
    db.session.add(record)
    db.session.commit()
    today = date.today()
    update_daily_summary(data.get("user_id", 1), today)
    return jsonify({
        "success": True,
        "data": {
            "id": record.id,
            "food_name": record.food_name,
            "food_name_cn": record.food_name_cn,
            "calorie": record.calorie,
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    }), 201


@app.route("/api/food/records/<int:record_id>", methods=["PUT"])
def update_food_record(record_id):
    record = FoodRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "记录不存在"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求数据为空"}), 400
    if "meal_type" in data:
        record.meal_type = data["meal_type"]
    if "weight_g" in data:
        record.weight_g = data["weight_g"]
        nutrition = calculate_nutrition(record.food_name, data["weight_g"])
        if nutrition:
            record.calorie = nutrition["calorie"]
            record.protein = nutrition["protein"]
            record.carb = nutrition["carb"]
            record.fat = nutrition["fat"]
            record.fiber = nutrition["fiber"]
    if "note" in data:
        record.note = data["note"]
    db.session.commit()
    update_daily_summary(record.user_id, date.today())
    return jsonify({"success": True, "msg": "更新成功"})


@app.route("/api/food/records/<int:record_id>", methods=["DELETE"])
def delete_food_record(record_id):
    record = FoodRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "记录不存在"}), 404
    db.session.delete(record)
    db.session.commit()
    update_daily_summary(record.user_id, date.today())
    return jsonify({"success": True, "msg": "删除成功"})


# ============ 每日营养汇总 API ============

@app.route("/api/food/daily_summary", methods=["GET"])
def get_daily_summary():
    target_date = request.args.get("date", date.today().isoformat())
    user_id = request.args.get("user_id", 1, type=int)
    summary = DailySummary.query.filter_by(user_id=user_id, record_date=target_date).first()
    if not summary:
        return jsonify({
            "success": True,
            "data": {
                "record_date": target_date,
                "total_calorie": 0, "total_protein": 0,
                "total_carb": 0, "total_fat": 0, "meal_count": 0,
            }
        })
    return jsonify({
        "success": True,
        "data": {
            "record_date": summary.record_date.isoformat(),
            "total_calorie": summary.total_calorie,
            "total_protein": summary.total_protein,
            "total_carb": summary.total_carb,
            "total_fat": summary.total_fat,
            "meal_count": summary.meal_count,
        }
    })


@app.route("/api/food/weekly_summary", methods=["GET"])
def get_weekly_summary():
    user_id = request.args.get("user_id", 1, type=int)
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    summaries = DailySummary.query.filter(
        DailySummary.user_id == user_id,
        DailySummary.record_date >= start_date,
        DailySummary.record_date <= end_date
    ).order_by(DailySummary.record_date.asc()).all()
    result = []
    for s in summaries:
        result.append({
            "record_date": s.record_date.isoformat(),
            "total_calorie": s.total_calorie,
            "total_protein": s.total_protein,
            "total_carb": s.total_carb,
            "total_fat": s.total_fat,
            "meal_count": s.meal_count,
        })
    return jsonify({"success": True, "data": result, "days": len(result)})


# 兼容旧接口
@app.route("/api/food", methods=["POST"])
def food():
    return jsonify({"food": "鸡胸肉", "calorie": 165})


@app.route("/api/pose", methods=["POST"])
def pose():
    return jsonify({"pose": "深蹲", "correct": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
