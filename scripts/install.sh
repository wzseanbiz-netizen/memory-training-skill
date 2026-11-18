#!/bin/bash
# 记忆法训练助手 —— 一键安装网页版到桌面
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
APP_DIR="$REPO_DIR/app"
DESKTOP_DIR="$HOME/桌面"

if [ ! -f "$APP_DIR/index.html" ]; then
  echo "未找到 $APP_DIR/index.html，请先运行: cd app && python3 build_web.py" >&2
  exit 1
fi

mkdir -p "$DESKTOP_DIR"

# 复制网页版到桌面
cp "$APP_DIR/index.html" "$DESKTOP_DIR/记忆法训练助手.html"

# 创建桌面启动器
cat > "$DESKTOP_DIR/记忆法训练助手.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=记忆法训练助手
Comment=记数字、记单词、记古诗词、记短文 —— 手机电脑通用，离线可用
Exec=xdg-open "$DESKTOP_DIR/记忆法训练助手.html"
Icon=applications-office
Terminal=false
Categories=Education;
EOF

chmod +x "$DESKTOP_DIR/记忆法训练助手.desktop"

echo "安装完成："
echo "  网页版：$DESKTOP_DIR/记忆法训练助手.html"
echo "  桌面图标：$DESKTOP_DIR/记忆法训练助手.desktop"
echo "双击桌面图标即可在浏览器中使用。"
