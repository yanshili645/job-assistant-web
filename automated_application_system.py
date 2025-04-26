#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能求职助手 - 自动申请系统
研究主要招聘网站的申请流程，实现自动填表和提交功能，以及申请状态跟踪
"""

import os
import json
import time
import random
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class AutomatedApplicationSystem:
    """自动申请系统类，用于自动填表和提交简历到招聘网站"""
    
    def __init__(self, data_dir="/home/ubuntu/job_data"):
        """初始化自动申请系统
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self.applications_dir = os.path.join(data_dir, "applications")
        self.history_file = os.path.join(data_dir, "application_history.json")
        self.ensure_directories()
        self.history = self.load_history()
        self.browser = None
        
    def ensure_directories(self):
        """确保必要的目录存在"""
        for directory in [self.data_dir, self.applications_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"创建目录: {directory}")
    
    def load_history(self):
        """加载申请历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载申请历史失败: {e}")
                return []
        return []
    
    def save_history(self):
        """保存申请历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存申请历史失败: {e}")
    
    def initialize_browser(self, headless=True):
        """初始化浏览器
        
        Args:
            headless: 是否使用无头模式
            
        Returns:
            bool: 初始化是否成功
        """
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
            
            self.browser = webdriver.Chrome(options=chrome_options)
            self.browser.implicitly_wait(10)
            print("浏览器初始化成功")
            return True
        except Exception as e:
            print(f"浏览器初始化失败: {e}")
            return False
    
    def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            try:
                self.browser.quit()
                print("浏览器已关闭")
            except Exception as e:
                print(f"关闭浏览器失败: {e}")
            finally:
                self.browser = None
    
    def extract_resume_data(self, resume_file):
        """从简历文件中提取申请所需的数据
        
        Args:
            resume_file: 简历文件路径
            
        Returns:
            dict: 提取的简历数据
        """
        try:
            with open(resume_file, 'r', encoding='utf-8') as f:
                resume_text = f.read()
        except Exception as e:
            print(f"读取简历文件失败: {e}")
            return {}
        
        # 提取基本信息
        resume_data = {}
        
        # 提取姓名
        name_match = resume_text.split('\n')[0].strip()
        if name_match:
            full_name = name_match
            name_parts = full_name.split()
            if len(name_parts) > 1:
                resume_data["first_name"] = name_parts[0]
                resume_data["last_name"] = name_parts[-1]
                if len(name_parts) > 2:
                    resume_data["middle_name"] = " ".join(name_parts[1:-1])
            else:
                resume_data["first_name"] = full_name
                resume_data["last_name"] = ""
        
        # 提取电话
        phone_match = re.search(r'Phone number: ([\+\d\s\(\)-]+)', resume_text)
        if phone_match:
            resume_data["phone"] = phone_match.group(1).strip()
        
        # 提取邮箱
        email_match = re.search(r'Email address: ([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', resume_text)
        if email_match:
            resume_data["email"] = email_match.group(1).strip()
        
        # 提取地址
        address_match = re.search(r'Home: (.*?)(?:\n|$)', resume_text)
        if address_match:
            resume_data["location"] = address_match.group(1).strip()
        
        # 提取当前职位
        current_role_match = re.search(r'ABOUT ME\s+(.*?)with', resume_text)
        if current_role_match:
            resume_data["current_title"] = current_role_match.group(1).strip()
        
        # 提取工作经验
        experiences = []
        experience_sections = re.findall(r'(.*?)\s+\[\s+(.*?)\s+–\s+(.*?)\s+\].*?City:\s+(.*?)\s+\|\s+Country:\s+(.*?)(?:\n|$)(.*?)(?=\n\n|\Z)', resume_text, re.DOTALL)
        for company, start_date, end_date, city, country, description in experience_sections:
            if "WORK EXPERIENCE" in company:
                continue
            experiences.append({
                "company": company.strip(),
                "title": "",  # 需要从描述中提取
                "start_date": start_date.strip(),
                "end_date": end_date.strip(),
                "location": f"{city.strip()}, {country.strip()}",
                "description": description.strip()
            })
            
            # 尝试从描述中提取职位
            title_match = re.search(r'(.*?)\n', description)
            if title_match:
                experiences[-1]["title"] = title_match.group(1).strip()
        
        resume_data["experiences"] = experiences
        
        # 提取教育背景
        education = []
        education_sections = re.findall(r'(.*?)\s+\[\s+(.*?)\s+–\s+(.*?)\s+\].*?City:\s+(.*?)\s+\|\s+Country:\s+(.*?)(?:\n|$)', resume_text)
        for school, start_date, end_date, city, country in education_sections:
            if "EDUCATION AND TRAINING" in school:
                continue
            education.append({
                "school": school.strip(),
                "degree": "",  # 需要从其他部分提取
                "field": "",   # 需要从其他部分提取
                "start_date": start_date.strip(),
                "end_date": end_date.strip(),
                "location": f"{city.strip()}, {country.strip()}"
            })
        
        # 尝试从其他部分提取学位和专业
        degree_sections = re.findall(r'(Master|Bachelor|PhD|Doctorate).*?of (.*?) in (.*?)\n', resume_text)
        for i, (degree_type, degree_field, school_info) in enumerate(degree_sections):
            if i < len(education):
                education[i]["degree"] = degree_type.strip()
                education[i]["field"] = degree_field.strip()
        
        resume_data["education"] = education
        
        # 提取技能
        skills = []
        skills_section = re.search(r'DIGITAL SKILLS\s+(.*?)HOBBIES AND INTERESTS', resume_text, re.DOTALL)
        if skills_section:
            skills_text = skills_section.group(1)
            skills = re.findall(r'[A-Za-z\+\.\s]+', skills_text)
            skills = [s.strip() for s in skills if s.strip()]
        
        resume_data["skills"] = skills
        
        # 提取语言能力
        languages = []
        language_section = re.search(r'LANGUAGE SKILLS\s+(.*?)DIGITAL SKILLS', resume_text, re.DOTALL)
        if language_section:
            language_text = language_section.group(1)
            # 提取语言
            lang_matches = re.findall(r'([A-Za-z]+)\s+LISTENING ([A-Z]\d)', language_text)
            for lang, level in lang_matches:
                languages.append({
                    "language": lang.strip(),
                    "level": level.strip()
                })
        
        resume_data["languages"] = languages
        
        return resume_data
    
    def apply_linkedin(self, job_url, resume_file, cover_letter_file=None, credentials=None):
        """在LinkedIn上申请工作
        
        Args:
            job_url: 工作URL
            resume_file: 简历文件路径
            cover_letter_file: 求职信文件路径，默认为None
            credentials: LinkedIn登录凭据，格式为{"email": "xxx", "password": "xxx"}
            
        Returns:
            dict: 申请结果
        """
        if not self.browser and not self.initialize_browser():
            return {"success": False, "message": "浏览器初始化失败"}
        
        result = {
            "success": False,
            "message": "",
            "job_url": job_url,
            "platform": "LinkedIn",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # 检查是否已登录
            self.browser.get("https://www.linkedin.com")
            time.sleep(2)
            
            # 如果未登录且提供了凭据，则登录
            if "Sign in" in self.browser.page_source and credentials:
                self.linkedin_login(credentials)
            
            # 如果仍未登录，返回错误
            if "Sign in" in self.browser.page_source:
                result["message"] = "LinkedIn需要登录才能申请工作"
                return result
            
            # 访问工作页面
            self.browser.get(job_url)
            time.sleep(3)
            
            # 检查是否是有效的工作页面
            if "This job is no longer available" in self.browser.page_source:
                result["message"] = "此工作已不可用"
                return result
            
            # 查找申请按钮
            try:
                apply_button = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='jobdetails_topcard_inapply']"))
                )
                apply_button.click()
                time.sleep(2)
            except TimeoutException:
                # 尝试其他可能的申请按钮
                try:
                    apply_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Easy Apply')]")
                    apply_button.click()
                    time.sleep(2)
                except NoSuchElementException:
                    result["message"] = "找不到申请按钮，可能需要在LinkedIn网站上申请"
                    return result
            
            # 提取简历数据
            resume_data = self.extract_resume_data(resume_file)
            
            # 填写申请表单
            # 注意：LinkedIn的申请表单可能有多个步骤，且字段可能因工作而异
            # 这里提供一个基本框架，实际应用中可能需要更复杂的逻辑
            
            # 检查是否有联系信息步骤
            if "Contact info" in self.browser.page_source:
                # 填写联系信息
                self.fill_linkedin_contact_info(resume_data)
                
                # 点击下一步
                next_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                next_button.click()
                time.sleep(2)
            
            # 检查是否有简历上传步骤
            if "Resume" in self.browser.page_source or "CV" in self.browser.page_source:
                # 上传简历
                resume_upload = self.browser.find_element(By.XPATH, "//input[@type='file']")
                resume_upload.send_keys(os.path.abspath(resume_file))
                time.sleep(3)
                
                # 点击下一步
                next_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                next_button.click()
                time.sleep(2)
            
            # 检查是否有求职信上传步骤
            if "Cover letter" in self.browser.page_source and cover_letter_file:
                # 上传求职信
                cover_letter_upload = self.browser.find_element(By.XPATH, "//input[@type='file']")
                cover_letter_upload.send_keys(os.path.abspath(cover_letter_file))
                time.sleep(3)
                
                # 点击下一步
                next_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                next_button.click()
                time.sleep(2)
            
            # 检查是否有附加问题
            if "questions" in self.browser.page_source.lower():
                # 回答附加问题
                self.answer_linkedin_questions(resume_data)
                
                # 点击下一步
                next_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                next_button.click()
                time.sleep(2)
            
            # 检查是否有审核步骤
            if "Review" in self.browser.page_source:
                # 点击提交按钮
                submit_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
                submit_button.click()
                time.sleep(5)
            
            # 检查是否申请成功
            if "Application submitted" in self.browser.page_source or "已提交申请" in self.browser.page_source:
                result["success"] = True
                result["message"] = "申请成功提交"
            else:
                result["message"] = "申请可能未成功提交，请手动检查"
            
            # 截图保存申请状态
            screenshot_path = os.path.join(self.applications_dir, f"linkedin_application_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            self.browser.save_screenshot(screenshot_path)
            result["screenshot"] = screenshot_path
            
            return result
            
        except Exception as e:
            result["message"] = f"申请过程中出错: {str(e)}"
            return result
    
    def linkedin_login(self, credentials):
        """登录LinkedIn
        
        Args:
            credentials: 登录凭据，格式为{"email": "xxx", "password": "xxx"}
            
        Returns:
            bool: 登录是否成功
        """
        try:
            # 访问登录页面
            self.browser.get("https://www.linkedin.com/login")
            time.sleep(2)
            
            # 填写邮箱
            email_input = self.browser.find_element(By.ID, "username")
            email_input.clear()
            email_input.send_keys(credentials["email"])
            
            # 填写密码
            password_input = self.browser.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(credentials["password"])
            
            # 点击登录按钮
            login_button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # 等待登录完成
            time.sleep(5)
            
            # 检查是否登录成功
            if "feed" in self.browser.current_url or "mynetwork" in self.browser.current_url:
                print("LinkedIn登录成功")
                return True
            else:
                print("LinkedIn登录失败")
                return False
                
        except Exception as e:
            print(f"LinkedIn登录过程中出错: {str(e)}")
            return False
    
    def fill_linkedin_contact_info(self, resume_data):
        """填写LinkedIn联系信息表单
        
        Args:
            resume_data: 简历数据
            
        Returns:
            bool: 填写是否成功
        """
        try:
            # 填写名字
            if "first_name" in resume_data:
                first_name_input = self.browser.find_element(By.NAME, "firstName")
                first_name_input.clear()
                first_name_input.send_keys(resume_data["first_name"])
            
            # 填写姓氏
            if "last_name" in resume_data:
                last_name_input = self.browser.find_element(By.NAME, "lastName")
                last_name_input.clear()
                last_name_input.send_keys(resume_data["last_name"])
            
            # 填写邮箱
            if "email" in resume_data:
                email_input = self.browser.find_element(By.NAME, "email")
                em
(Content truncated due to size limit. Use line ranges to read in chunks)