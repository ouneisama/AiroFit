# AiroFit

前后端分离的 AI 健身辅助系统。摄像头实时识别人体姿态完成动作计数，拍照上传由视觉大模型识别食物并估算热量与三大营养素，训练与饮食数据通过图表可视化。

## 功能

| 模块 | 说明 |
| --- | --- |
| 动作识别计数 | MediaPipe Pose Landmarker 实时检测人体关节点，按角度阈值判定深蹲、俯卧撑、臂展等动作并自动计数，后端以 MJPEG 视频流回传画面 |
| 食物热量识别 | 上传食物照片，调用通义千问 qwen-vl-plus 视觉大模型识别食物种类与分量，结合本地食物营养库换算热量、蛋白质、碳水、脂肪、膳食纤维 |
| 饮食记录 | 按早餐 / 午餐 / 晚餐记录，支持手动修正重量后重新换算营养数据 |
| 社区 | 发布图文动态，支持多图上传 |
| 数据可视化 | ECharts 展示热量摄入与训练趋势 |
| 肌肉图谱与教学视频 | 前端内置肌肉部位示意图与各动作示范视频 |

## 技术栈

- **前端**：Vue 3 + Vite、Element Plus、ECharts、Axios
- **后端**：Flask、Flask-SQLAlchemy（SQLite）、Flask-CORS、OpenCV
- **AI 能力**：MediaPipe Pose Landmarker Lite（本地姿态模型）、通义千问 qwen-vl-plus（视觉识别）

## 目录结构

```
AiroFit/
├── backend/
│   ├── app.py                    # 社区、饮食记录 REST API 与 AI 食物识别
│   ├── appAI.py                  # 摄像头实时动作识别服务（MJPEG 视频流 + 计数接口）
│   ├── pose_landmarker_lite.task # MediaPipe 姿态模型文件
│   ├── requirements.txt
│   └── templates/index.html
└── frontend/
    ├── src/views/                # Home / Exercise / ActionJudge / FoodCalorie /
    │                             # Community / MuscleMap / VideoZone / Profile / Setting
    ├── public/videos/            # 动作示范视频
    └── vite.config.js
```

## 本地运行

### 1. 后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

复制环境变量模板并填入自己的 Key（Windows 用 `copy .env.example .env`）：

```bash
cp .env.example .env
```

启动服务：

```bash
python app.py       # 主服务，http://127.0.0.1:5000
python appAI.py     # 动作识别服务，摄像头画面与计数接口
```

> 注意：两个服务默认都监听 5000 端口。需要同时运行时，请把其中一个改为 5001，并同步修改前端 `ActionJudge.vue` 中的请求地址。

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 Vite 输出的地址（默认 http://localhost:5173）。

## 获取 API Key

食物识别依赖阿里云百炼的通义千问视觉模型：

1. 打开 https://dashscope.console.aliyun.com/ 注册并创建 API Key
2. 将 Key 填入 `backend/.env` 的 `DASHSCOPE_API_KEY`

未配置 Key 时，食物识别功能不可用，其余功能不受影响。

## 环境要求

- Python 3.9+
- Node.js 18+
- 摄像头（仅动作识别功能需要）

## License

[MIT](LICENSE)
