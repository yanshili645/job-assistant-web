#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能求职助手 - 启动脚本
用于安装依赖并启动智能求职助手系统
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """检查并安装依赖"""
    print("正在检查依赖...")
    
    # 必要的依赖列表
    dependencies = [
        "gradio",
        "pandas",
        "selenium",
        "nltk",
        "scikit-learn",
        "python-jobspy",
        "markdown",
        "webdriver-manager"
    ]
    
    # 检查并安装缺失的依赖
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} 已安装")
        except ImportError:
            print(f"✗ {dep} 未安装，正在安装...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} 安装完成")
    
    # 安装NLTK数据
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✓ NLTK数据已下载")
    except Exception as e:
        print(f"✗ NLTK数据下载失败: {e}")
    
    print("所有依赖检查完成！")

def setup_environment():
    """设置环境"""
    print("正在设置环境...")
    
    # 创建必要的目录
    directories = [
        "job_data",
        "resumes",
        "cover_letters",
        "job_data/applications"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ 创建目录: {directory}")
    
    print("环境设置完成！")

def start_assistant():
    """启动智能求职助手"""
    print("正在启动智能求职助手...")
    
    try:
        # 检查主程序文件是否存在
        if not os.path.exists("smart_job_assistant.py"):
            print("✗ 主程序文件不存在！")
            return False
        
        # 启动主程序
        subprocess.Popen([sys.executable, "smart_job_assistant.py"])
        print("✓ 智能求职助手已启动！")
        print("请在浏览器中访问显示的URL地址")
        return True
    except Exception as e:
        print(f"✗ 启动失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("智能求职助手 - 启动程序")
    print("=" * 50)
    
    # 检查并安装依赖
    check_dependencies()
    
    # 设置环境
    setup_environment()
    
    # 启动助手
    if start_assistant():
        print("\n系统已成功启动！")
        print("您可以通过Web界面使用以下功能：")
        print("1. 简历管理 - 上传和优化您的简历")
        print("2. 工作搜索 - 从多个招聘网站搜索工作")
        print("3. 工作匹配 - 将您的简历与工作机会进行匹配")
        print("4. 自荐信生成 - 为特定职位生成自荐信")
        print("5. 自动申请 - 自动向匹配的职位提交申请")
        print("\n按Ctrl+C可以停止系统")
    else:
        print("\n系统启动失败，请检查错误信息")

if __name__ == "__main__":
    main()
