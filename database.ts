// 数据库配置文件
// 这个文件设置了D1数据库的初始化和连接

import { D1Database } from '@cloudflare/workers-types';

// 获取数据库连接
export function getDatabase(env: any): D1Database {
  return env.DB;
}

// 初始化数据库
export async function initializeDatabase(db: D1Database) {
  try {
    // 检查数据库是否已初始化
    const tablesExist = await checkTablesExist(db);
    
    if (!tablesExist) {
      // 创建所有必要的表
      await createTables(db);
      console.log('数据库表创建成功');
    } else {
      console.log('数据库表已存在');
    }
    
    return true;
  } catch (error) {
    console.error('初始化数据库时出错:', error);
    return false;
  }
}

// 检查数据库表是否存在
async function checkTablesExist(db: D1Database): Promise<boolean> {
  try {
    // 查询sqlite_master表检查表是否存在
    const result = await db.prepare(
      "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    ).all();
    
    return result.results.length > 0;
  } catch (error) {
    console.error('检查数据库表时出错:', error);
    return false;
  }
}

// 创建所有必要的表
async function createTables(db: D1Database) {
  // 用户表
  await db.exec(`
    CREATE TABLE users (
      id TEXT PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      name TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);
  
  // 简历表
  await db.exec(`
    CREATE TABLE resumes (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      name TEXT NOT NULL,
      content TEXT NOT NULL,
      analysis TEXT,
      score INTEGER,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
  `);
  
  // 工作搜索表
  await db.exec(`
    CREATE TABLE job_searches (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      search_term TEXT NOT NULL,
      location TEXT,
      job_type TEXT,
      is_remote BOOLEAN,
      results_count INTEGER,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
  `);
  
  // 工作表
  await db.exec(`
    CREATE TABLE jobs (
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
    )
  `);
  
  // 工作匹配表
  await db.exec(`
    CREATE TABLE job_matches (
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
    )
  `);
  
  // 自荐信表
  await db.exec(`
    CREATE TABLE cover_letters (
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
    )
  `);
  
  // 申请表
  await db.exec(`
    CREATE TABLE applications (
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
    )
  `);
}
