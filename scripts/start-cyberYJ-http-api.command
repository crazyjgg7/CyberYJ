#!/bin/bash

# CyberYJ HTTP API 启动脚本（供微信小程序联调）

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   CyberYJ HTTP API 启动脚本${NC}"
echo -e "${BLUE}   Wechat 小程序对接服务${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

PROJECT_DIR="/Users/apple/dev/CyberYJ"
PORT="${1:-8080}"
HOST="${HOST:-0.0.0.0}"

echo -e "${GREEN}[1/6]${NC} 切换到项目目录: $PROJECT_DIR"
cd "$PROJECT_DIR" || {
  echo -e "${RED}错误: 无法找到项目目录${NC}"
  exit 1
}

echo -e "${GREEN}[2/6]${NC} 检查虚拟环境..."
if [ ! -d "venv" ]; then
  echo -e "${YELLOW}      虚拟环境不存在，正在创建...${NC}"
  /Users/apple/opt/anaconda3/envs/py310/bin/python3.10 -m venv venv || {
    echo -e "${RED}错误: 创建虚拟环境失败${NC}"
    exit 1
  }
fi

echo -e "${GREEN}[3/6]${NC} 激活虚拟环境..."
source venv/bin/activate
echo "      Python 版本: $(python --version)"

echo -e "${GREEN}[4/6]${NC} 检查 HTTP API 依赖..."
if ! python -c "import fastapi, uvicorn" 2>/dev/null; then
  echo -e "${YELLOW}      fastapi/uvicorn 未安装，正在安装 api 依赖...${NC}"
  pip install -e ".[api]" || {
    echo -e "${RED}错误: 安装 api 依赖失败${NC}"
    exit 1
  }
fi
echo -e "${GREEN}      ✓ 依赖检查通过${NC}"

echo -e "${GREEN}[5/6]${NC} 启动前自检 (路由检查)..."
if ! PYTHONPATH="$PROJECT_DIR/src" python - <<'PY'
from cyberYJ.api.http_app import create_app

app = create_app()
paths = {route.path for route in app.routes}
assert "/v1/divination/interpret" in paths
print("self-check ok: /v1/divination/interpret")
PY
then
  echo -e "${RED}错误: 自检失败，未发现 /v1/divination/interpret${NC}"
  exit 1
fi

if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo -e "${YELLOW}      警告: 端口 ${PORT} 已被占用，自动切换到 18080${NC}"
  PORT=18080
fi

echo -e "${GREEN}[6/6]${NC} 启动 HTTP API..."
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   API 正在运行: http://${HOST}:${PORT}${NC}"
echo -e "${BLUE}   接口: POST /v1/divination/interpret${NC}"
echo -e "${BLUE}   按 Ctrl+C 停止服务${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

export PYTHONPATH="$PROJECT_DIR/src"
python -m uvicorn cyberYJ.api.http_app:create_app --factory --host "$HOST" --port "$PORT"

echo ""
echo -e "${RED}API 已停止${NC}"
echo ""
read -p "按任意键关闭窗口..." -n1 -s

