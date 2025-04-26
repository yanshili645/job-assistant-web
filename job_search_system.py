#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能求职助手 - 工作搜索系统
基于JobSpy库从多个招聘网站搜索工作信息
"""

import os
import csv
import json
import pandas as pd
from datetime import datetime
from jobspy import scrape_jobs

class JobSearchSystem:
    """工作搜索系统类，用于从多个招聘网站搜索工作信息"""
    
    def __init__(self, data_dir="/home/ubuntu/job_data"):
        """初始化工作搜索系统
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self.search_history_file = os.path.join(data_dir, "search_history.json")
        self.ensure_data_dir()
        self.search_history = self.load_search_history()
        
    def ensure_data_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"创建数据目录: {self.data_dir}")
    
    def load_search_history(self):
        """加载搜索历史"""
        if os.path.exists(self.search_history_file):
            try:
                with open(self.search_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载搜索历史失败: {e}")
                return []
        return []
    
    def save_search_history(self):
        """保存搜索历史"""
        try:
            with open(self.search_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存搜索历史失败: {e}")
    
    def search_jobs(self, search_term, location=None, site_names=None, 
                   job_type=None, is_remote=None, results_wanted=50, 
                   hours_old=72, country=None, description_format="markdown"):
        """搜索工作
        
        Args:
            search_term: 搜索关键词
            location: 位置
            site_names: 搜索网站列表，默认为所有支持的网站
            job_type: 工作类型 (fulltime, parttime, internship, contract)
            is_remote: 是否远程工作
            results_wanted: 每个网站返回的结果数量
            hours_old: 过滤多少小时内发布的工作
            country: 国家（用于Indeed和Glassdoor）
            description_format: 描述格式 (markdown, html)
            
        Returns:
            DataFrame: 工作搜索结果
        """
        # 默认搜索所有支持的网站
        if site_names is None:
            site_names = ["linkedin", "indeed", "glassdoor", "google"]
        
        # 准备搜索参数
        search_params = {
            "site_name": site_names,
            "search_term": search_term,
            "results_wanted": results_wanted,
            "description_format": description_format,
            "hours_old": hours_old
        }
        
        # 添加可选参数
        if location:
            search_params["location"] = location
        if job_type:
            search_params["job_type"] = job_type
        if is_remote is not None:
            search_params["is_remote"] = is_remote
        if country:
            search_params["country_indeed"] = country
            
        # 如果搜索Google Jobs，添加google_search_term参数
        if "google" in site_names:
            google_search_term = f"{search_term} jobs"
            if location:
                google_search_term += f" near {location}"
            google_search_term += " since yesterday"
            search_params["google_search_term"] = google_search_term
            
        # 记录搜索开始时间
        start_time = datetime.now()
        print(f"开始搜索工作: {search_term}")
        
        try:
            # 执行搜索
            jobs_df = scrape_jobs(**search_params)
            
            # 记录搜索结束时间和结果数量
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            job_count = len(jobs_df)
            print(f"搜索完成，找到 {job_count} 个工作，耗时 {duration:.2f} 秒")
            
            # 保存搜索结果
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = os.path.join(self.data_dir, f"jobs_{timestamp}.csv")
            jobs_df.to_csv(result_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
            print(f"搜索结果已保存到: {result_file}")
            
            # 更新搜索历史
            search_record = {
                "timestamp": timestamp,
                "search_term": search_term,
                "location": location,
                "site_names": site_names,
                "job_type": job_type,
                "is_remote": is_remote,
                "results_count": job_count,
                "result_file": result_file,
                "duration": duration
            }
            self.search_history.append(search_record)
            self.save_search_history()
            
            return jobs_df
            
        except Exception as e:
            print(f"搜索工作失败: {e}")
            return pd.DataFrame()
    
    def get_recent_searches(self, limit=10):
        """获取最近的搜索记录
        
        Args:
            limit: 返回的记录数量限制
            
        Returns:
            list: 最近的搜索记录列表
        """
        return self.search_history[-limit:] if self.search_history else []
    
    def load_search_result(self, result_file):
        """加载搜索结果
        
        Args:
            result_file: 搜索结果文件路径
            
        Returns:
            DataFrame: 搜索结果
        """
        try:
            return pd.read_csv(result_file)
        except Exception as e:
            print(f"加载搜索结果失败: {e}")
            return pd.DataFrame()
    
    def filter_jobs(self, jobs_df, keywords=None, exclude_keywords=None, 
                   min_salary=None, max_salary=None, companies=None,
                   locations=None, job_types=None):
        """过滤工作结果
        
        Args:
            jobs_df: 工作结果DataFrame
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
        filtered_df = jobs_df.copy()
        
        # 关键词过滤
        if keywords:
            keyword_filters = []
            for keyword in keywords:
                # 在标题、公司名称和描述中搜索关键词
                title_filter = filtered_df['TITLE'].str.contains(keyword, case=False, na=False)
                company_filter = filtered_df['COMPANY'].str.contains(keyword, case=False, na=False)
                desc_filter = filtered_df['DESCRIPTION'].str.contains(keyword, case=False, na=False)
                keyword_filters.append(title_filter | company_filter | desc_filter)
            
            if keyword_filters:
                combined_filter = keyword_filters[0]
                for f in keyword_filters[1:]:
                    combined_filter = combined_filter & f
                filtered_df = filtered_df[combined_filter]
        
        # 排除关键词
        if exclude_keywords:
            for keyword in exclude_keywords:
                # 排除标题、公司名称和描述中包含关键词的结果
                title_filter = ~filtered_df['TITLE'].str.contains(keyword, case=False, na=False)
                company_filter = ~filtered_df['COMPANY'].str.contains(keyword, case=False, na=False)
                desc_filter = ~filtered_df['DESCRIPTION'].str.contains(keyword, case=False, na=False)
                filtered_df = filtered_df[title_filter & company_filter & desc_filter]
        
        # 薪资过滤
        if min_salary is not None and 'MAX_AMOUNT' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['MAX_AMOUNT'] >= min_salary]
        
        if max_salary is not None and 'MIN_AMOUNT' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['MIN_AMOUNT'] <= max_salary]
        
        # 公司过滤
        if companies:
            company_filter = filtered_df['COMPANY'].isin(companies)
            filtered_df = filtered_df[company_filter]
        
        # 位置过滤
        if locations:
            location_filters = []
            for location in locations:
                city_filter = filtered_df['CITY'].str.contains(location, case=False, na=False)
                state_filter = filtered_df['STATE'].str.contains(location, case=False, na=False)
                location_filters.append(city_filter | state_filter)
            
            if location_filters:
                combined_filter = location_filters[0]
                for f in location_filters[1:]:
                    combined_filter = combined_filter | f
                filtered_df = filtered_df[combined_filter]
        
        # 工作类型过滤
        if job_types and 'JOB_TYPE' in filtered_df.columns:
            job_type_filter = filtered_df['JOB_TYPE'].isin(job_types)
            filtered_df = filtered_df[job_type_filter]
        
        return filtered_df
    
    def extract_skills_from_jobs(self, jobs_df, top_n=20):
        """从工作描述中提取常见技能
        
        Args:
            jobs_df: 工作结果DataFrame
            top_n: 返回的技能数量
            
        Returns:
            dict: 技能及其出现频率
        """
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
            "ios", "android", "mobile", "web", "frontend", "backend", "fullstack"
        ]
        
        # 初始化技能计数器
        skill_counts = {skill: 0 for skill in common_skills}
        
        # 遍历工作描述，计算技能出现次数
        for desc in jobs_df['DESCRIPTION'].dropna():
            desc_lower = desc.lower()
            for skill in common_skills:
                if skill in desc_lower:
                    skill_counts[skill] += 1
        
        # 过滤掉未出现的技能，并按出现次数排序
        skill_counts = {k: v for k, v in skill_counts.items() if v > 0}
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
        
        # 返回出现频率最高的技能
        return dict(sorted_skills[:top_n])
    
    def generate_job_search_report(self, jobs_df, output_file=None):
        """生成工作搜索报告
        
        Args:
            jobs_df: 工作结果DataFrame
            output_file: 输出文件路径，默认为None（返回报告文本）
            
        Returns:
            str: 报告文本（如果output_file为None）
        """
        if jobs_df.empty:
            report = "# 工作搜索报告\n\n**没有找到匹配的工作**"
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report)
            return report
        
        # 计算基本统计信息
        job_count = len(jobs_df)
        site_counts = jobs_df['SITE'].value_counts().to_dict()
        company_counts = jobs_df['COMPANY'].value_counts().head(10).to_dict()
        location_counts = jobs_df['CITY'].value_counts().head(10).to_dict()
        
        # 提取常见技能
        skills = self.extract_skills_from_jobs(jobs_df)
        
        # 生成报告
        report = f"""# 工作搜索报告

## 概述
- **总工作数量**: {job_count}
- **搜索时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 来源网站分布
"""
        
        for site, count in site_counts.items():
            report += f"- **{site}**: {count} ({count/job_count*100:.1f}%)\n"
        
        report += "\n## 热门公司\n"
        for company, count in company_counts.items():
            report += f"- **{company}**: {count} 个职位\n"
        
        report += "\n## 热门地区\n"
        for location, count in location_counts.items():
            report += f"- **{location}**: {count} 个职位\n"
        
        report += "\n## 常见技能需求\n"
        for skill, count in skills.items():
            report += f"- **{skill}**: 出现在 {count} 个职位描述中 ({count/job_count*100:.1f}%)\n"
        
        report += "\n## 示例职位\n"
        # 选择前5个职位作为示例
        for i, (_, job) in enumerate(jobs_df.head(5).iterrows()):
            report += f"""
### {i+1}. {job['TITLE']} - {job['COMPANY']}
- **位置**: {job['CITY']}, {job['STATE']}
- **来源**: {job['SITE']}
- **链接**: {job['JOB_URL']}
"""
            # 添加薪资信息（如果有）
            if pd.notna(job.get('MIN_AMOUNT')) or pd.notna(job.get('MAX_AMOUNT')):
                min_amount = job.get('MIN_AMOUNT', 'N/A')
                max_amount = job.get('MAX_AMOUNT', 'N/A')
                interval = job.get('INTERVAL', 'yearly')
                report += f"- **薪资**: {min_amount} - {max_amount} ({interval})\n"
        
        # 保存报告（如果指定了输出文件）
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report

# 测试代码
if __name__ == "__main__":
    # 创建工作搜索系统实例
    job_search = JobSearchSystem()
    
    # 测试搜索功能
    search_term = "AI Product Manager"
    location = "Shanghai, China"
    site_names = ["linkedin", "indeed"]
    
    # 执行搜索
    jobs = job_search.search_jobs(
        search_term=search_term,
        location=location,
        site_names=site_names,
        results_wanted=10,
        country="China"
    )
    
    # 生成报告
    if not jobs.empty:
        report_file = os.path.join(job_search.data_dir, "search_report.md")
        job_search.generate_job_search_report(jobs, report_file)
        print(f"报告已生成: {report_file}")
