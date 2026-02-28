#!/bin/bash

# GitHub Deploy Script
# 自动推送到 https://github.com/leonxiao91/openclaw-workspace

REPO_URL="https://github.com/leonxiao91/openclaw-workspace.git"
BRANCH="main"

# 获取提交信息（如果没有提供则使用默认）
COMMIT_MSG="${1:-Update}"

# 检查是否在 git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "错误: 当前目录不是 git 仓库"
    exit 1
fi

# 获取仓库根目录
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

echo "📦 开始部署到 GitHub..."
echo "📂 目录: $REPO_ROOT"
echo "📝 提交信息: $COMMIT_MSG"

# 检查远程仓库是否已配置
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 添加远程仓库..."
    git remote add origin "$REPO_URL"
fi

# 设置远程仓库 URL（确保使用正确的仓库）
git remote set-url origin "$REPO_URL"

# 添加所有更改
echo "📋 添加文件..."
git add -A

# 检查是否有更改
if git diff --staged --quiet; then
    echo "✅ 没有新更改需要提交"
else
    # 提交更改
    echo "💾 提交更改..."
    git commit -m "$COMMIT_MSG"
    
    # 推送到 GitHub
    echo "🚀 推送到 GitHub..."
    git push -u origin "$BRANCH"
    
    echo "✅ 部署完成!"
    echo "🔗 查看仓库: $REPO_URL"
fi
