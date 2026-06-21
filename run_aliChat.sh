#!/bin/bash
# 启动脚本：确保中文支持后运行 aliChat.py

echo "=== 阿里云千问问答机器人启动脚本 ==="
echo ""

# 设置中文支持
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

echo "✓ 已设置中文支持"
echo "  LANG=$LANG"
echo "  LC_ALL=$LC_ALL"
echo ""

# 切换到项目目录
cd /Users/andy_mac/PycharmProjects/xai

echo "✓ 已切换到项目目录"
echo ""
echo "=== 启动问答机器人 ==="
echo ""

# 运行Python脚本
python app/ai/openAi/ali/aliChat.py
