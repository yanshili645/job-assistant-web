// 数据库迁移文件
// 这个文件包含初始化数据库的SQL语句

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建简历表
CREATE TABLE IF NOT EXISTS resumes (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  name TEXT NOT NULL,
  content TEXT NOT NULL,
  analysis TEXT,
  score INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建工作搜索表
CREATE TABLE IF NOT EXISTS job_searches (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  search_term TEXT NOT NULL,
  location TEXT,
  job_type TEXT,
  is_remote BOOLEAN,
  results_count INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建工作表
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT NOT NULL,
  description TEXT NOT NULL,
  salary INTEGER,
  job_type TEXT,
  posted_date TEXT,
  site TEXT,
  url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建工作匹配表
CREATE TABLE IF NOT EXISTS job_matches (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  resume_id TEXT NOT NULL,
  job_id TEXT NOT NULL,
  overall_score INTEGER NOT NULL,
  skill_score INTEGER,
  experience_score INTEGER,
  education_score INTEGER,
  language_score INTEGER,
  match_reasons TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (resume_id) REFERENCES resumes(id),
  FOREIGN KEY (job_id) REFERENCES jobs(id)
);

-- 创建自荐信表
CREATE TABLE IF NOT EXISTS cover_letters (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  job_id TEXT,
  resume_id TEXT,
  template_id TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (job_id) REFERENCES jobs(id),
  FOREIGN KEY (resume_id) REFERENCES resumes(id)
);

-- 创建申请表
CREATE TABLE IF NOT EXISTS applications (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  job_id TEXT NOT NULL,
  resume_id TEXT NOT NULL,
  cover_letter_id TEXT,
  status TEXT NOT NULL,
  response TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (job_id) REFERENCES jobs(id),
  FOREIGN KEY (resume_id) REFERENCES resumes(id),
  FOREIGN KEY (cover_letter_id) REFERENCES cover_letters(id)
);

-- 插入一些测试数据
INSERT INTO users (id, email, name) VALUES 
('user-1', 'test@example.com', '测试用户');

-- 插入一些模板数据
INSERT INTO cover_letters (id, user_id, template_id, content) VALUES
('template-standard', 'user-1', 'standard', '标准模板内容'),
('template-creative', 'user-1', 'creative', '创意模板内容'),
('template-technical', 'user-1', 'technical', '技术模板内容'),
('template-executive', 'user-1', 'executive', '高管模板内容'),
('template-academic', 'user-1', 'academic', '学术模板内容');
