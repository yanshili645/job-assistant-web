#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能求职助手 - 工作匹配算法
基于简历内容和职位要求进行匹配评分，帮助用户找到最适合的工作机会
"""

import os
import json
import re
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class JobMatchingSystem:
    """工作匹配系统类，用于基于简历内容和职位要求进行匹配评分"""
    
    def __init__(self, data_dir="/home/ubuntu/job_data"):
        """初始化工作匹配系统
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self.matches_dir = os.path.join(data_dir, "matches")
        self.history_file = os.path.join(data_dir, "matching_history.json")
        self.ensure_directories()
        self.history = self.load_history()
        self.initialize_nltk()
        
    def ensure_directories(self):
        """确保必要的目录存在"""
        for directory in [self.data_dir, self.matches_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"创建目录: {directory}")
    
    def load_history(self):
        """加载匹配历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载匹配历史失败: {e}")
                return []
        return []
    
    def save_history(self):
        """保存匹配历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存匹配历史失败: {e}")
    
    def initialize_nltk(self):
        """初始化NLTK资源"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        except Exception as e:
            print(f"初始化NLTK资源失败: {e}")
            # 使用基本的停用词列表作为备选
            self.stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
                              'when', 'where', 'how', 'who', 'which', 'this', 'that', 'these', 'those',
                              'then', 'just', 'so', 'than', 'such', 'both', 'through', 'about', 'for',
                              'is', 'of', 'while', 'during', 'to', 'from', 'in', 'on', 'at', 'by', 'with'}
            self.lemmatizer = None
    
    def preprocess_text(self, text):
        """预处理文本
        
        Args:
            text: 输入文本
            
        Returns:
            str: 预处理后的文本
        """
        if not text:
            return ""
        
        # 转换为小写
        text = text.lower()
        
        # 移除特殊字符和数字
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        
        # 分词
        tokens = word_tokenize(text) if hasattr(self, 'lemmatizer') else text.split()
        
        # 移除停用词
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # 词形还原
        if hasattr(self, 'lemmatizer') and self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        # 重新组合为文本
        return ' '.join(tokens)
    
    def extract_resume_features(self, resume_file):
        """从简历文件中提取特征
        
        Args:
            resume_file: 简历文件路径
            
        Returns:
            dict: 提取的简历特征
        """
        try:
            with open(resume_file, 'r', encoding='utf-8') as f:
                resume_text = f.read()
        except Exception as e:
            print(f"读取简历文件失败: {e}")
            return {}
        
        # 提取基本信息
        resume_features = {}
        
        # 提取姓名
        name_match = re.search(r'^([A-Za-z\s]+)', resume_text)
        if name_match:
            resume_features["name"] = name_match.group(1).strip()
        
        # 提取当前职位
        current_role_match = re.search(r'ABOUT ME\s+(.*?)with', resume_text)
        if current_role_match:
            resume_features["current_role"] = current_role_match.group(1).strip()
        
        # 提取工作经验年限
        experience_match = re.search(r'with (\d+\+?) years of experience', resume_text)
        if experience_match:
            experience_text = experience_match.group(1).strip()
            # 处理"10+"这样的格式
            if experience_text.endswith('+'):
                resume_features["years_of_experience"] = int(experience_text[:-1])
            else:
                resume_features["years_of_experience"] = int(experience_text)
        
        # 提取行业
        industry_match = re.search(r'experience in (.*?) development', resume_text)
        if industry_match:
            resume_features["industry"] = industry_match.group(1).strip()
        else:
            resume_features["industry"] = "AI和语音技术"
        
        # 提取技能
        skills = []
        skills_section = re.search(r'DIGITAL SKILLS\s+(.*?)HOBBIES AND INTERESTS', resume_text, re.DOTALL)
        if skills_section:
            skills_text = skills_section.group(1)
            # 提取技能列表
            skills = re.findall(r'[A-Za-z\+\.\s]+', skills_text)
            skills = [s.strip() for s in skills if s.strip()]
        
        resume_features["skills"] = skills
        
        # 提取教育背景
        education = []
        education_section = re.search(r'EDUCATION AND TRAINING\s+(.*?)LANGUAGE SKILLS', resume_text, re.DOTALL)
        if education_section:
            education_text = education_section.group(1)
            # 提取学位
            degrees = re.findall(r'(Master|Bachelor|PhD|Doctorate).*?of.*?in (.*?)\n', education_text)
            for degree_type, field in degrees:
                education.append({
                    "degree": degree_type.strip(),
                    "field": field.strip()
                })
        
        resume_features["education"] = education
        
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
        
        resume_features["languages"] = languages
        
        # 提取工作经验
        experiences = []
        experience_sections = re.findall(r'(.*?)\s+\[\s+(.*?)\s+–\s+(.*?)\s+\].*?City:\s+(.*?)\s+\|\s+Country:\s+(.*?)(?:\n|$)(.*?)(?=\n\n|\Z)', resume_text, re.DOTALL)
        for company, start_date, end_date, city, country, description in experience_sections:
            if "WORK EXPERIENCE" in company:
                continue
            experiences.append({
                "company": company.strip(),
                "start_date": start_date.strip(),
                "end_date": end_date.strip(),
                "location": f"{city.strip()}, {country.strip()}",
                "description": description.strip()
            })
        
        resume_features["experiences"] = experiences
        
        # 提取项目经验
        projects = []
        project_sections = re.findall(r'PROJECTS.*?\[\s+(.*?)\s+–\s+(.*?)\s+\](.*?)(?=\[\s+\d|EDUCATION|$)', resume_text, re.DOTALL)
        for start_date, end_date, description in project_sections:
            # 提取项目名称
            project_name_match = re.search(r'(.*?)•', description)
            project_name = project_name_match.group(1).strip() if project_name_match else "未命名项目"
            
            projects.append({
                "name": project_name,
                "start_date": start_date.strip(),
                "end_date": end_date.strip(),
                "description": description.strip()
            })
        
        resume_features["projects"] = projects
        
        # 预处理简历全文，用于文本相似度匹配
        resume_features["full_text"] = self.preprocess_text(resume_text)
        
        return resume_features
    
    def extract_job_features(self, job_data):
        """从职位数据中提取特征
        
        Args:
            job_data: 职位数据（字典或DataFrame行）
            
        Returns:
            dict: 提取的职位特征
        """
        # 如果输入是DataFrame行，转换为字典
        if isinstance(job_data, pd.Series):
            job_data = job_data.to_dict()
        
        # 提取基本信息
        job_features = {
            "title": job_data.get("TITLE", ""),
            "company": job_data.get("COMPANY", ""),
            "location": f"{job_data.get('CITY', '')}, {job_data.get('STATE', '')}",
            "job_type": job_data.get("JOB_TYPE", ""),
            "salary_min": job_data.get("MIN_AMOUNT", None),
            "salary_max": job_data.get("MAX_AMOUNT", None),
            "salary_interval": job_data.get("INTERVAL", "yearly"),
            "url": job_data.get("JOB_URL", ""),
            "site": job_data.get("SITE", "")
        }
        
        # 获取职位描述
        description = job_data.get("DESCRIPTION", "")
        job_features["description"] = description
        
        # 提取所需技能
        required_skills = self.extract_skills_from_description(description)
        job_features["required_skills"] = required_skills
        
        # 提取所需经验年限
        experience_years = self.extract_experience_requirement(description)
        job_features["required_experience"] = experience_years
        
        # 提取所需教育背景
        education = self.extract_education_requirement(description)
        job_features["required_education"] = education
        
        # 提取所需语言能力
        languages = self.extract_language_requirement(description)
        job_features["required_languages"] = languages
        
        # 预处理职位描述，用于文本相似度匹配
        job_features["processed_description"] = self.preprocess_text(description)
        
        return job_features
    
    def extract_skills_from_description(self, description):
        """从职位描述中提取所需技能
        
        Args:
            description: 职位描述文本
            
        Returns:
            list: 提取的技能列表
        """
        if not description:
            return []
        
        # 常见技能关键词列表
        common_skills = [
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin", 
            "golang", "rust", "typescript", "scala", "r", "matlab", "sql", "nosql", "mongodb", 
            "postgresql", "mysql", "oracle", "aws", "azure", "gcp", "docker", "kubernetes", 
            "jenkins", "git", "github", "gitlab", "ci/cd", "agile", "scrum", "kanban", 
            "jira", "confluence", "react", "angular", "vue", "node.js", "django", "flask", 
            "spring", "hibernate", "asp.net", "laravel", "tensorflow", "pytorch", "keras", 
            "scikit-learn", "pandas", "numpy", "hadoop", "spark", "kafka", "redis", "elasticsearch",
            "ai", "machine learning", "deep learning", "nlp", "computer vision", "data science",
            "big data", "data analysis", "data visualization", "tableau", "power bi", "excel",
            "product management", "project management", "ux/ui", "figma", "sketch", "adobe xd",
            "photoshop", "illustrator", "indesign", "after effects", "premiere pro",
            "devops", "sre", "security", "networking", "linux", "windows", "macos",
            "rest api", "graphql", "soap", "microservices", "serverless", "blockchain",
            "ios", "android", "mobile", "web", "frontend", "backend", "fullstack",
            "communication", "leadership", "teamwork", "problem solving", "critical thinking",
            "time management", "creativity", "adaptability", "emotional intelligence",
            "negotiation", "presentation", "writing", "research", "analytical", "detail-oriented",
            "customer service", "sales", "marketing", "finance", "accounting", "hr", "recruiting",
            "operations", "strategy", "consulting", "business development", "entrepreneurship"
        ]
        
        # 将描述转为小写
        desc_lower = description.lower()
        
        # 查找匹配的技能
        found_skills = []
        for skill in common_skills:
            if skill in desc_lower:
                found_skills.append(skill)
        
        # 尝试从技能相关段落中提取更多技能
        skill_sections = re.findall(r'(?:skills|requirements|qualifications)(?::|required|include).*?(?:\n\n|\Z)', description, re.IGNORECASE | re.DOTALL)
        if skill_sections:
            for section in skill_sections:
                # 提取列表项
                list_items = re.findall(r'(?:•|\*|-|\d+\.)\s+(.*?)(?:\n|$)', section)
                for item in list_items:
                    # 检查是否包含常见技能
                    item_lower = item.lower()
                    for skill in common_skills:
                        if skill in item_lower and skill not in found_skills:
                            found_skills.append(skill)
        
        return found_skills
    
    def extract_experience_requirement(self, description):
        """从职位描述中提取所需经验年限
        
        Args:
            description: 职位描述文本
            
        Returns:
            int: 所需经验年限，如果未找到则返回0
        """
        if not description:
            return 0
        
        # 常见的经验要求表达方式
        experience_patterns = [
            r'(\d+)\+?\s*(?:years|yrs).*?experience',
            r'(\d+)\+?\s*(?:years|yrs).*?work experience',
            r'experience.*?(\d+)\+?\s*(?:years|yrs)',
            r'minimum.*?(\d+)\+?\s*(?:years|yrs)',
            r'at least.*?(\d+)\+?\s*(?:years|yrs)'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                years = match.group(1)
                return int(years)
        
        # 如果没有找到明确的年限要求，检查是否有初级/中级/高级的描述
        if re.search(r'senior|experienced|lead', description, re.IGNORECASE):
            return 5
        elif re.search(r'mid-level|intermediate', description, re.IGNORECASE):
            return 3
        elif re.search(r'junior|entry-level|graduate', description, re.IGNORECASE):
            return 1
        
        return 0
    
    def extract_education_requirement(self, description):
        """从职位描述中提取所需教育背景
        
        Args:
            description: 职位描述文本
            
        Returns:
            dict: 所需教育背景
        """
        if not description:
            return {"level": "none", "fields": []}
        
        # 检查学位要求
        degree_level = "none"
        if re.search(r'phd|doctorate|doctoral', description, re.IGNORECASE):
            degree_level = "phd"
        elif re.search(r'master|ms|msc|ma|mba', description, re.IGNORECASE):
            degree_level = "master"
        elif re.search(r'bachelor|bs|bsc|ba|undergraduate', description, re.IGNORECASE):
            degree_level = "bachelor"
        elif re.search(r'associate|diploma', description, re.IGNORECASE):
            degree_level = "associate"
        
        # 提取学科领域
        fields = []
        field_patterns = [
            r'degree in (.*?)(?:\.|\,|\;|\n|or |and |required|preferred)',
            r'background in (.*?)(?:\.|\,|\;|\n|or |and |required|preferred)',
            r'education in (.*?)(?:\.|\,|\;|\n|or |and |required|preferred)'
        ]
        
        for pattern in field_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            for match in matches:
                # 清理并添加到领域列表
                field = match.strip()
                if field and len(field) < 100:  # 避免匹配过长的文本
                    fields.append(field)
        
        return {"level": degree_level, "fields": fields}
    
    def extract_language_requirement(self, description):
(Content truncated due to size limit. Use line ranges to read in chunks)