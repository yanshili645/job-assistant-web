#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能求职助手 - 自荐信生成器
基于简历和职位描述自动生成定制化的求职信
"""

import os
import json
import re
import pandas as pd
from datetime import datetime

class CoverLetterGenerator:
    """自荐信生成器类，用于基于简历和职位描述生成定制化的求职信"""
    
    def __init__(self, data_dir="/home/ubuntu/job_data", templates_dir="/home/ubuntu/templates"):
        """初始化自荐信生成器
        
        Args:
            data_dir: 数据存储目录
            templates_dir: 模板存储目录
        """
        self.data_dir = data_dir
        self.templates_dir = templates_dir
        self.cover_letters_dir = os.path.join(data_dir, "cover_letters")
        self.history_file = os.path.join(data_dir, "cover_letter_history.json")
        self.ensure_directories()
        self.history = self.load_history()
        self.create_default_templates()
        
    def ensure_directories(self):
        """确保必要的目录存在"""
        for directory in [self.data_dir, self.templates_dir, self.cover_letters_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"创建目录: {directory}")
    
    def load_history(self):
        """加载生成历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载生成历史失败: {e}")
                return []
        return []
    
    def save_history(self):
        """保存生成历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存生成历史失败: {e}")
    
    def create_default_templates(self):
        """创建默认的自荐信模板"""
        templates = {
            "standard": self._create_standard_template(),
            "enthusiastic": self._create_enthusiastic_template(),
            "professional": self._create_professional_template(),
            "technical": self._create_technical_template(),
            "creative": self._create_creative_template(),
        }
        
        for name, content in templates.items():
            template_file = os.path.join(self.templates_dir, f"{name}_template.md")
            if not os.path.exists(template_file):
                try:
                    with open(template_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"创建默认模板: {template_file}")
                except Exception as e:
                    print(f"创建默认模板失败: {e}")
    
    def _create_standard_template(self):
        """创建标准自荐信模板"""
        return """# 标准自荐信模板

{current_date}

{recruiter_name}
{company_name}
{company_address}

尊敬的{recruiter_name}：

我怀着极大的热情申请贵公司发布的{job_title}职位。作为一名拥有{years_of_experience}年{industry}行业经验的{current_role}，我相信我的技能和经验与贵公司的需求高度匹配。

在我目前担任{current_company}的{current_role}期间，我{achievement_1}。此前，我在{previous_company}工作时，成功{achievement_2}。这些经历使我具备了{skill_1}、{skill_2}和{skill_3}等关键技能，这些正是{job_title}职位所需要的。

我对{company_name}的{company_value_or_product}特别感兴趣，并且认为我的{relevant_experience}经验可以为贵公司带来价值。我期待能够加入贵公司的团队，为{company_goal}贡献自己的力量。

感谢您考虑我的申请。我期待有机会进一步讨论我如何为{company_name}做出贡献。

此致

敬礼

{applicant_name}
{applicant_phone}
{applicant_email}
"""
    
    def _create_enthusiastic_template(self):
        """创建热情型自荐信模板"""
        return """# 热情型自荐信模板

{current_date}

{recruiter_name}
{company_name}
{company_address}

亲爱的{recruiter_name}：

当我看到贵公司招聘{job_title}的职位时，我感到无比兴奋！作为{company_name}产品和服务的忠实粉丝，我一直在关注贵公司的创新发展，并梦想能够成为这个令人赞叹的团队的一员。

我在{industry}行业已有{years_of_experience}年的经验，目前在{current_company}担任{current_role}。在这个角色中，我热情地{achievement_1}，并且成功地{achievement_2}。我相信这些经验完美地契合了贵公司{job_title}职位的需求。

贵公司的{company_value_or_product}深深地吸引了我，我渴望能够将我的{skill_1}、{skill_2}和{skill_3}技能带入贵公司，为{company_goal}贡献我的热情和创意。

我非常期待能有机会与您面谈，分享我对{industry}行业的见解，以及我如何能够为{company_name}的成功添砖加瓦。感谢您考虑我的申请！

热切期待您的回复！

{applicant_name}
{applicant_phone}
{applicant_email}
"""
    
    def _create_professional_template(self):
        """创建专业型自荐信模板"""
        return """# 专业型自荐信模板

{current_date}

{recruiter_name}
{company_name}
{company_address}

尊敬的{recruiter_name}：

我谨此申请贵公司的{job_title}职位。凭借我在{industry}行业{years_of_experience}年的专业经验，以及在{skill_1}、{skill_2}和{skill_3}方面的专长，我有信心能够为贵公司带来显著价值。

职业成就概述：

1. 在{current_company}担任{current_role}期间，我{achievement_1}，提高了{achievement_1_result}。
2. 在{previous_company}工作时，我领导团队{achievement_2}，实现了{achievement_2_result}。
3. 我具备丰富的{relevant_experience}经验，这与贵公司{job_title}职位的要求高度吻合。

我对{company_name}的{company_value_or_product}印象深刻，并且认同贵公司的{company_culture}文化。我相信我的专业背景和技能将使我能够立即为贵公司的{company_goal}做出贡献。

感谢您考虑我的申请。我期待有机会进一步讨论我如何能够支持贵公司的战略目标。

专业致敬，

{applicant_name}
{applicant_phone}
{applicant_email}
"""
    
    def _create_technical_template(self):
        """创建技术型自荐信模板"""
        return """# 技术型自荐信模板

{current_date}

{recruiter_name}
{company_name}
{company_address}

尊敬的{recruiter_name}：

我怀着极大的兴趣申请贵公司的{job_title}职位。作为一名拥有{years_of_experience}年经验的{current_role}，我具备了{job_title}所需的技术专长和解决问题的能力。

技术技能与成就：

- 技术专长：{skill_1}、{skill_2}、{skill_3}、{skill_4}、{skill_5}
- 在{current_company}工作期间，我{achievement_1}，使用{technical_tools_1}实现了{achievement_1_result}
- 在{previous_company}，我设计并实施了{achievement_2}，采用{technical_tools_2}，解决了{problem_solved}

我密切关注{industry}行业的最新技术发展，并不断更新我的技能库。贵公司在{company_value_or_product}方面的创新工作令我印象深刻，我渴望能够将我的技术知识和经验带入贵公司的团队。

我相信我的技术背景和解决问题的能力将使我成为贵公司{job_title}职位的理想人选。我期待有机会详细讨论我如何能够为{company_name}的技术目标做出贡献。

此致

{applicant_name}
{applicant_phone}
{applicant_email}
"""
    
    def _create_creative_template(self):
        """创建创意型自荐信模板"""
        return """# 创意型自荐信模板

{current_date}

嗨，{recruiter_name}！

想象一下：一个拥有{years_of_experience}年{industry}经验，精通{skill_1}、{skill_2}和{skill_3}的{current_role}加入了您的团队。这个人不仅带来了丰富的经验，还带来了创新的思维和解决问题的热情。这就是我——{applicant_name}，您的{job_title}职位的理想候选人。

我的职业旅程充满了创意和成就：

✨ 在{current_company}，我{achievement_1}，为公司带来了全新的视角
✨ 在{previous_company}，我打破常规，{achievement_2}，创造了令人惊叹的结果
✨ 我始终以{personal_value}为指导原则，这与{company_name}的{company_value_or_product}完美契合

{company_name}在{industry}行业的创新精神深深吸引了我。我渴望能够加入您的团队，为{company_goal}贡献我的创意和热情。

我期待着与您见面，分享更多关于我如何能够为{company_name}带来独特价值的想法！

创意无限，

{applicant_name}
{applicant_phone}
{applicant_email}

P.S. 我特别喜欢贵公司的{company_product_or_initiative}，这正是吸引我申请的原因之一！
"""
    
    def list_templates(self):
        """列出所有可用的模板"""
        templates = []
        for file in os.listdir(self.templates_dir):
            if file.endswith("_template.md"):
                template_name = file.replace("_template.md", "")
                template_path = os.path.join(self.templates_dir, file)
                templates.append({
                    "name": template_name,
                    "path": template_path
                })
        return templates
    
    def load_template(self, template_name):
        """加载指定的模板
        
        Args:
            template_name: 模板名称
            
        Returns:
            str: 模板内容
        """
        template_path = os.path.join(self.templates_dir, f"{template_name}_template.md")
        if not os.path.exists(template_path):
            print(f"模板不存在: {template_path}")
            return None
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"加载模板失败: {e}")
            return None
    
    def extract_job_details(self, job_data):
        """从职位数据中提取关键信息
        
        Args:
            job_data: 职位数据（字典或DataFrame行）
            
        Returns:
            dict: 提取的职位详情
        """
        # 如果输入是DataFrame行，转换为字典
        if isinstance(job_data, pd.Series):
            job_data = job_data.to_dict()
        
        # 提取基本信息
        job_details = {
            "job_title": job_data.get("TITLE", ""),
            "company_name": job_data.get("COMPANY", ""),
            "company_address": f"{job_data.get('CITY', '')}, {job_data.get('STATE', '')}",
            "job_description": job_data.get("DESCRIPTION", ""),
            "job_url": job_data.get("JOB_URL", ""),
            "job_type": job_data.get("JOB_TYPE", ""),
            "salary_min": job_data.get("MIN_AMOUNT", ""),
            "salary_max": job_data.get("MAX_AMOUNT", ""),
            "salary_interval": job_data.get("INTERVAL", "yearly")
        }
        
        # 从描述中提取关键技能
        skills = self.extract_skills_from_description(job_details["job_description"])
        job_details["required_skills"] = skills
        
        # 尝试从描述中提取公司信息
        company_info = self.extract_company_info(job_details["job_description"], job_details["company_name"])
        job_details.update(company_info)
        
        return job_details
    
    def extract_skills_from_description(self, description):
        """从职位描述中提取技能
        
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
        
        return found_skills
    
    def extract_company_info(self, description, company_name):
        """从职位描述中提取公司信息
        
        Args:
            description: 职位描述文本
            company_name: 公司名称
            
        Returns:
            dict: 提取的公司信息
        """
        if not description:
            return {}
        
        company_info = {
            "company_value_or_product": "",
            "company_culture": "",
            "company_goal": "",
            "company_product_or_initiative": ""
        }
        
        # 尝试提取公司价值观或产品
        value_patterns = [
            rf"{company_name}.*?(?:values|mission|vision).*?(?:is|are|includes) (.*?)\.",
            r"(?:Our|The) (?:values|mission|vision).*?(?:is|are|includes) (.*?)\.",
            rf"{company_name}.*?(?:specializes in|focuses on|provides) (.*?)\.",
            r"(?:Our|The) (?:company|organization).*?(?:specializes in|focuses on|provides) (.*?)\."
        ]
        
        for pattern in value_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                company_info["company_value_or_product"] = match.group(1).strip()
                break
        
        # 尝试提取公司文化
        culture_patterns = [
            rf"{company_name}.*?culture.*?(?:is|values) (.*?)\.",
            r"(?:Our|The) culture.*?(?:is|values) (.*?)\.",
            r"We (?:value|prioritize|focus on) (.*?) in our (?:team|workplace|environment)\."
        ]
        
        for pattern in culture_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                company_info["company_culture"] = match.group(1).strip()
                break
        
        # 尝试提取公司目标
        goal_patterns = [
            rf"{company_name}.*?(?:aims|strives|goals).*?(?:to|is|are) (.*?)\.",
            r"(?:Our|The) (?:aim|goal|mission).*?(?:is|are) (.*?)\.",
            r"We (?:aim|strive|work) to (.*?)\."
        ]
        
        for pattern in goal_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                company_info["company_goal"] = match.group(1).strip()
                break
        
        # 尝试提取公司产品或倡议
        product_patterns = [
            rf"{company_name}.*?(?:product|service|solution|platform) (.*?)\.",
            r"(?:Our|The) (?:product|service|solution|platform).*?(?:is|includes) (.*?)\.",
            rf"{company_name}.*?(?:recently|proudly) (?:launched|introduced|developed) (.*?)\.",
            r"We (?:recently|proudly) (?:launched|introduced|developed) (.*?)\."
        ]
        
        for pattern in product_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                company_info["company_product_or_initiative"] = match.group(1).strip()
                break
        
        # 如果没有提取到信息，使用默认值
        for key, value in company_info.items():
            if not value:
                if key == "company_value_or_product":
                    company_info[key] = f"{company_name}的产品和服务"
                elif key == "company_culture":
                    company_info[key] = "创新和协作"
                elif key == "company_goal":
                    company_info[key] = "行业领先目标"
                elif key == "company_product_or_initiative":
                    company_info[key] = "创新产品"
        
        return company_info
    
    def extract_resume_details(self, resume_file):
        """从简历文件中提取关键信息
        
        Args:
            resume_file: 简历文件路径
            
        Returns:
            dict: 提取的简历详情
        """
        try:
            with open(resume_file, 'r', encoding='utf-8') as f:
                resume_text = f.read()
        except Exception as e:
            print(f"读取简历文件失败: {e}")
            return {}
        
        # 提取基本信息
        resume_details = {}
        
        # 提取姓名
        name_match = re.search(r'^([A-Za-z\s]+)', resume_text)
        if name_match:
            resume_details["applicant_name"] = name_match.group(1).strip()
        
        # 提取电话
        phone_match = re.search(r'Phone number: ([\+\d\s\(\)-]+)', resume_text)
        if phone_match:
            resume_details["applicant_phone"] = phone_match.group(1).strip()
        
        # 提取邮箱
        email_match = re.search(r'Email address: ([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', resume_text)
        if email_match:
            resume_details["applicant_email"] = email_match.group(1).strip()
        
        # 提取当前职位
        current_role_match = re.search(r'ABOUT ME\s+(.*?)with', resume_text)
        if current_role_match:
            resume_details["current_role"] = current_role_match.group(1).strip()
        
        # 提取工作经验年限
        experience_match = re.search(r'with (\d+\+?) years of experience', resume_text)
        if experience_match:
            resume_details["years_of_experience
(Content truncated due to size limit. Use line ranges to read in chunks)