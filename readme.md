# ASR Service

语音识别（ASR）服务，基于 FastAPI 框架构建。

## 项目结构

```
asr_server/
├── app/
│   ├── api/                    # API 路由层
│   │   ├── __init__.py
│   │   └── v1/                 # API v1 版本
│   │       ├── __init__.py
│   │       └── asr.py          # ASR 相关接口
│   ├── core/                   # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py           # 配置管理
│   │   └── logger.py           # 日志配置
│   ├── models/                 # 数据模型
│   │   └── __init__.py
│   ├── schemas/                # Pydantic 模型
│   │   ├── __init__.py
│   │   └── asr.py
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   └── asr_service.py      # ASR 服务
│   ├── utils/                  # 工具函数
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py                 # FastAPI 应用入口
├── logs/                       # 日志目录
├── tests/                      # 测试目录
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── run.sh                      # 启动脚本
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

根据需要修改 `.env` 文件中的配置。

### 3. 启动服务

方式一：使用启动脚本

```bash
./run.sh
```

方式二：直接运行

```bash
python -m app.main
```

服务将在 `http://0.0.0.0:8696` 启动。

## API 文档

启动服务后，可以通过以下地址访问 API 文档：

- Swagger UI: http://localhost:port/docs
- ReDoc: http://localhost:port/redoc

## 主要接口

### 1. 语音识别

**接口**: `POST /api/v1/asr/transcribe`

**请求参数**:
- `file`: 音频文件 (multipart/form-data)
- `language`: 语言代码 (默认: zh)
- `sample_rate`: 采样率 (默认: 16000)
- `channels`: 声道数 (默认: 1)

**响应示例**:
```json
{
  "code": 0,
  "msg": "语音识别成功",
  "data": {
    "request_id": "xxxx112312r42redfd-dsafsa-qwfwefwe",
    "text": "没有别人了吧没有好嘞打扰了啊拜拜",
    "confidence": 0.785,
    "language": "zh",
    "duration": 0.0,
    "processing_time": 24.33
  },
  "timestamp": "2026-03-14T06:25:55.417893"
}
```

### 2. 健康检查

**接口**: `GET /api/v1/asr/health`

**响应示例**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2024-01-01T00:00:00"
}
```

## 架构说明

### 分层架构

1. **API 层** (`app/api/`): 处理 HTTP 请求和响应
2. **业务逻辑层** (`app/services/`): 核心业务逻辑实现
3. **数据模型层** (`app/schemas/`): 请求/响应数据验证
4. **核心配置** (`app/core/`): 配置管理和日志

### 设计原则

- **解耦合**: 各层职责明确，易于扩展和维护
- **健壮性**: 完善的错误处理和日志记录
- **可扩展性**: 模块化设计，便于添加新功能

## 开发说明

### 代码规范

项目使用以下工具进行代码规范管理：
- `black`: 代码格式化
- `ruff`: 代码检查

### 日志

日志文件存储在 `logs/` 目录下，按天轮转，保留 30 天。
