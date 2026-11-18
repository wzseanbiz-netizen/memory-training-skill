#!/bin/bash
# 上传记忆法训练助手到 GitHub
# 用法：先修改下方 REPO_URL 为你自己的仓库地址，再运行本脚本
set -e

REPO_URL="https://github.com/你的用户名/memory-training-skill.git"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
cd "$REPO_DIR"

if [ "$REPO_URL" = "https://github.com/你的用户名/memory-training-skill.git" ]; then
  echo "请先修改 scripts/upload-github.sh 中的 REPO_URL 为你自己的 GitHub 仓库地址。" >&2
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi

git push -u origin main
echo "上传完成。"
