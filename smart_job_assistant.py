#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能求职助手 - 主程序
整合所有组件并构建用户界面，提供完整的求职助手系统
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
import gradio as gr
import markdown
import re
import importlib.util

# 导入自定义模块
from job_search_system import JobSearchSystem
from cover_letter_generator import CoverLetterGenerator
from job_matching_system import JobMatchingSystem
from automated_application_system import AutomatedApplicationSystem

class SmartJobAssistant:
    """智能求职助手类，整合所有组件并提供用户界面"""
    
    def __init__(self, base_dir="/home/ubuntu"):
        """初始化智能求职助手
        
        Args:
            base_dir: 基础目录
        """
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "job_data")
        self.resume_dir = os.path.join(base_dir, "resumes")
        self.config_file = os.path.join(self.data_dir, "assistant_config.json")
        
        # 确保目录存在
        self.ensure_directories()
        
        # 加载配置
        self.config = self.load_config()
        
        # 初始化组件
        self.job_search = JobSearchSystem(self.data_dir)
        self.cover_letter_generator = CoverLetterGenerator(self.data_dir)
        self.job_matcher = JobMatchingSystem(self.data_dir)
        self.application_system = AutomatedApplicationSystem(self.data_dir)
        
        # 当前简历文件
        self.current_resume_file = self.config.get("current_resume_file", "")
        self.current_resume_content = ""
        if self.current_resume_file and os.path.exists(self.current_resume_file):
            with open(self.current_resume_file, 'r', encoding='utf-8') as f:
                self.current_resume_content = f.read()
        
        # 当前工作数据
        self.current_jobs_file = self.config.get("current_jobs_file", "")
        self.current_jobs_df = pd.DataFrame()
        if self.current_jobs_file and os.path.exists(self.current_jobs_file):
            try:
                self.current_jobs_df = pd.read_csv(self.current_jobs_file)
            except:
                pass
        
        # 当前匹配结果
        self.current_matches_file = self.config.get("current_matches_file", "")
        self.current_matches_df = pd.DataFrame()
        if self.current_matches_file and os.path.exists(self.current_matches_file):
            try:
                self.current_matches_df = pd.read_csv(self.current_matches_file)
            except:
                pass
    
    def ensure_directories(self):
        """确保必要的目录存在"""
        for directory in [self.data_dir, self.resume_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"创建目录: {directory}")
    
    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {e}")
                return {}
        return {}
    
    def save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def update_config(self, key, value):
        """更新配置
        
        Args:
            key: 配置键
            value: 配置值
        """
        self.config[key] = value
        self.save_config()
    
    def set_current_resume(self, resume_file):
        """设置当前简历
        
        Args:
            resume_file: 简历文件路径
            
        Returns:
            str: 简历内容
        """
        if not os.path.exists(resume_file):
            return "简历文件不存在"
        
        self.current_resume_file = resume_file
        self.update_config("current_resume_file", resume_file)
        
        try:
            with open(resume_file, 'r', encoding='utf-8') as f:
                self.current_resume_content = f.read()
            return self.current_resume_content
        except Exception as e:
            return f"读取简历文件失败: {e}"
    
    def save_improved_resume(self, content, filename=None):
        """保存改进的简历
        
        Args:
            content: 简历内容
            filename: 文件名，默认为None（自动生成）
            
        Returns:
            str: 保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"improved_resume_{timestamp}.md"
        
        file_path = os.path.join(self.resume_dir, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 更新当前简历
            self.current_resume_file = file_path
            self.current_resume_content = content
            self.update_config("current_resume_file", file_path)
            
            return file_path
        except Exception as e:
            print(f"保存简历失败: {e}")
            return None
    
    def search_jobs(self, search_term, location=None, site_names=None, 
                   job_type=None, is_remote=None, results_wanted=50, 
                   hours_old=72, country=None):
        """搜索工作
        
        Args:
            search_term: 搜索关键词
            location: 位置
            site_names: 搜索网站列表
            job_type: 工作类型
            is_remote: 是否远程工作
            results_wanted: 每个网站返回的结果数量
            hours_old: 过滤多少小时内发布的工作
            country: 国家
            
        Returns:
            DataFrame: 工作搜索结果
        """
        # 转换site_names为列表
        if site_names and isinstance(site_names, str):
            site_names = [site.strip() for site in site_names.split(",")]
        
        # 执行搜索
        jobs_df = self.job_search.search_jobs(
            search_term=search_term,
            location=location,
            site_names=site_names,
            job_type=job_type,
            is_remote=is_remote,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country=country
        )
        
        # 更新当前工作数据
        if not jobs_df.empty:
            self.current_jobs_df = jobs_df
            
            # 保存到文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            jobs_file = os.path.join(self.data_dir, f"jobs_{timestamp}.csv")
            jobs_df.to_csv(jobs_file, index=False)
            
            # 更新配置
            self.current_jobs_file = jobs_file
            self.update_config("current_jobs_file", jobs_file)
        
        return jobs_df
    
    def filter_jobs(self, jobs_df=None, keywords=None, exclude_keywords=None, 
                   min_salary=None, max_salary=None, companies=None,
                   locations=None, job_types=None):
        """过滤工作结果
        
        Args:
            jobs_df: 工作结果DataFrame，默认为当前工作数据
            keywords: 包含的关键词列表
            exclude_keywords: 排除的关键词列表
            min_salary: 最低薪资
            max_salary: 最高薪资
            companies: 公司列表
            locations: 位置列表
            job_types: 工作类型列表
            
        Returns:
            DataFrame: 过滤后的工作结果
        """
        # 使用当前工作数据（如果未提供）
        if jobs_df is None:
            jobs_df = self.current_jobs_df
        
        if jobs_df.empty:
            return pd.DataFrame()
        
        # 转换关键词为列表
        if keywords and isinstance(keywords, str):
            keywords = [kw.strip() for kw in keywords.split(",")]
        
        if exclude_keywords and isinstance(exclude_keywords, str):
            exclude_keywords = [kw.strip() for kw in exclude_keywords.split(",")]
        
        if companies and isinstance(companies, str):
            companies = [c.strip() for c in companies.split(",")]
        
        if locations and isinstance(locations, str):
            locations = [loc.strip() for loc in locations.split(",")]
        
        if job_types and isinstance(job_types, str):
            job_types = [jt.strip() for jt in job_types.split(",")]
        
        # 执行过滤
        filtered_df = self.job_search.filter_jobs(
            jobs_df=jobs_df,
            keywords=keywords,
            exclude_keywords=exclude_keywords,
            min_salary=min_salary,
            max_salary=max_salary,
            companies=companies,
            locations=locations,
            job_types=job_types
        )
        
        return filtered_df
    
    def generate_job_search_report(self, jobs_df=None):
        """生成工作搜索报告
        
        Args:
            jobs_df: 工作结果DataFrame，默认为当前工作数据
            
        Returns:
            str: 报告文本
            str: 报告文件路径
        """
        # 使用当前工作数据（如果未提供）
        if jobs_df is None:
            jobs_df = self.current_jobs_df
        
        if jobs_df.empty:
            return "没有工作数据生成报告", None
        
        # 生成报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.data_dir, f"job_search_report_{timestamp}.md")
        
        report_text = self.job_search.generate_job_search_report(jobs_df, report_file)
        
        return report_text, report_file
    
    def match_jobs(self, resume_file=None, jobs_df=None):
        """匹配工作
        
        Args:
            resume_file: 简历文件路径，默认为当前简历
            jobs_df: 工作DataFrame，默认为当前工作数据
            
        Returns:
            DataFrame: 匹配结果DataFrame
        """
        # 使用当前简历（如果未提供）
        if resume_file is None:
            resume_file = self.current_resume_file
        
        if not resume_file or not os.path.exists(resume_file):
            return pd.DataFrame()
        
        # 使用当前工作数据（如果未提供）
        if jobs_df is None:
            jobs_df = self.current_jobs_df
        
        if jobs_df.empty:
            return pd.DataFrame()
        
        # 执行匹配
        matches_df = self.job_matcher.match_jobs(resume_file, jobs_df)
        
        # 更新当前匹配结果
        if not matches_df.empty:
            self.current_matches_df = matches_df
            
            # 保存到文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            matches_file = os.path.join(self.data_dir, f"job_matches_{timestamp}.csv")
            matches_df.to_csv(matches_file, index=False)
            
            # 更新配置
            self.current_matches_file = matches_file
            self.update_config("current_matches_file", matches_file)
        
        return matches_df
    
    def generate_match_report(self, matches_df=None, resume_file=None):
        """生成匹配报告
        
        Args:
            matches_df: 匹配结果DataFrame，默认为当前匹配结果
            resume_file: 简历文件路径，默认为当前简历
            
        Returns:
            str: 报告文本
            str: 报告文件路径
        """
        # 使用当前匹配结果（如果未提供）
        if matches_df is None:
            matches_df = self.current_matches_df
        
        if matches_df.empty:
            return "没有匹配结果生成报告", None
        
        # 使用当前简历（如果未提供）
        if resume_file is None:
            resume_file = self.current_resume_file
        
        if not resume_file or not os.path.exists(resume_file):
            return "简历文件不存在", None
        
        # 生成报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.data_dir, f"match_report_{timestamp}.md")
        
        report_text = self.job_matcher.generate_match_report(matches_df, resume_file, report_file)
        
        return report_text, report_file
    
    def generate_cover_letter(self, job_data, resume_file=None, template_name="standard", recruiter_name="招聘经理"):
        """生成自荐信
        
        Args:
            job_data: 工作数据（字典或DataFrame行）
            resume_file: 简历文件路径，默认为当前简历
            template_name: 模板名称
            recruiter_name: 招聘人员姓名
            
        Returns:
            str: 生成的自荐信内容
            str: 保存的文件路径
        """
        # 使用当前简历（如果未提供）
        if resume_file is None:
            resume_file = self.current_resume_file
        
        if not resume_file or not os.path.exists(resume_file):
            return "简历文件不存在", None
        
        # 生成自荐信
        cover_letter, file_path = self.cover_letter_generator.generate_cover_letter(
            template_name=template_name,
            job_data=job_data,
            resume_file=resume_file,
            recruiter_name=recruiter_name
        )
        
        return cover_letter, file_path
    
    def apply_job(self, job_data, resume_file=None, cover_letter_file=None, credentials=None):
        """申请工作
        
        Args:
            job_data: 工作数据（字典或DataFrame行）
            resume_file: 简历文件路径，默认为当前简历
            cover_letter_file: 求职信文件路径
            credentials: 登录凭据
            
        Returns:
            dict: 申请结果
        """
        # 使用当前简历（如果未提供）
        if resume_file is None:
            resume_file = self.current_resume_file
        
        if not resume_file or not os.path.exists(resume_file):
            return {"success": False, "message": "简历文件不存在"}
        
        # 申请工作
        result = self.application_system.apply_job(
            job_data=job_data,
            resume_file=resume_file,
            cover_letter_file=cover_letter_file,
            credentials=credentials
        )
        
        return result
    
    def batch_apply(self, jobs_df=None, resume_file=None, cover_letter_file=None, credentials=None, max_applications=10):
        """批量申请工作
        
        Args:
            jobs_df: 工作DataFrame，默认为当前匹配结果
            resume_file: 简历文件路径，默认为当前简历
            cover_letter_file: 求职信文件路径
            credentials: 登录凭据
            max_applications: 最大申请数量
            
        Returns:
            list: 申请结果列表
        """
        # 使用当前匹配结果（如果未提供）
        if jobs_df is None:
            jobs_df = self.current_matches_df
        
        if jobs_df.empty:
            return [{"success": False, "message": "没有匹配的工作进行申请"}]
        
        # 使用当前简历（如果未提供）
        if resume_file is None:
            resume_file = self.current_resume_file
        
        if not resume_file or not os.path.exists(resume_file):
            return [{"success": False, "message": "简历文件不存在"}]
        
        # 批量申请
        results = self.application_system.batch_apply(
            jobs_df=jobs_df,
            resume_file=resume_file,
            cover_letter_file=cover_letter_file,
            credentials=credentials,
            max_applications=max_applications
        )
        
        return results
    
    def generate_application_report(self, application_results):
        """生成申请报告
        
        Args:
            application_results: 申请结果列表
            
        Returns:
            str: 报告文本
            str: 报告文件路径
        """
        if not application_results:
            return "没有申请结果生成报告", None
        
        # 生成报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.data_dir, f"application_report_{timestamp}.md")
        
        report_text = self.application_system.generate_application_report(application_results, report_file)
        
        return report_text, report_file
    
    def track_application_status(self, credentials=None):
        """跟踪申请状态
        
        Args:
            credentials: 登录凭据
            
        Returns:
            dict: 更新的申请状态
        """
        # 跟踪状态
        status_updates = self.application_system.track_application_status(credentials)
        
        return status_updates
    
    def generate_status_report(self):
        """生成申请状态报告
        
        Returns:
            str: 报告文本
            str: 报告文件路径
        """
        # 生成报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.data_dir, f"status_report_{timestamp}.md")
        
        report_text = self.application_system.generate_status_report(report_file)
        
        return report_text, report_file
    
    def build_ui(self):
        """构建用户界面
        
        Returns:
            gr.Blocks: Gradio界面
        """
     
(Content truncated due to size limit. Use line ranges to read in chunks)