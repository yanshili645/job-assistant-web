// 这个文件包含API路由处理函数，用于处理简历相关的请求

import { NextRequest, NextResponse } from 'next/server';

// 处理简历上传
export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const resumeFile = formData.get('resume') as File;
    
    if (!resumeFile) {
      return NextResponse.json(
        { error: '没有提供简历文件' },
        { status: 400 }
      );
    }
    
    // 读取文件内容
    const fileContent = await resumeFile.text();
    
    // 在实际应用中，这里应该将文件保存到数据库或存储系统
    // 并调用简历分析服务来处理简历内容
    
    // 模拟简历分析结果
    const analysis = analyzeResume(fileContent);
    
    return NextResponse.json({
      success: true,
      message: '简历上传成功',
      fileName: resumeFile.name,
      fileSize: resumeFile.size,
      analysis
    });
  } catch (error) {
    console.error('简历上传处理错误:', error);
    return NextResponse.json(
      { error: '处理简历时出错' },
      { status: 500 }
    );
  }
}

// 获取简历列表
export async function GET(request: NextRequest) {
  try {
    // 在实际应用中，这里应该从数据库获取用户的简历列表
    
    // 模拟简历列表
    const resumes = [
      {
        id: 'resume-1',
        name: 'software_engineer_resume.pdf',
        uploadDate: '2025-04-20',
        size: 245678,
        status: 'analyzed'
      },
      {
        id: 'resume-2',
        name: 'data_scientist_resume.pdf',
        uploadDate: '2025-04-15',
        size: 198432,
        status: 'analyzed'
      }
    ];
    
    return NextResponse.json({
      success: true,
      resumes
    });
  } catch (error) {
    console.error('获取简历列表错误:', error);
    return NextResponse.json(
      { error: '获取简历列表时出错' },
      { status: 500 }
    );
  }
}

// 简单的简历分析函数（示例）
function analyzeResume(content: string) {
  // 在实际应用中，这里应该使用更复杂的NLP和ML算法来分析简历
  
  // 简单的关键词提取
  const skills = extractSkills(content);
  const education = extractEducation(content);
  const experience = extractExperience(content);
  
  // 生成改进建议
  const suggestions = generateSuggestions(content, skills, experience);
  
  return {
    skills,
    education,
    experience,
    suggestions,
    score: calculateResumeScore(skills, education, experience)
  };
}

// 提取技能（示例）
function extractSkills(content: string) {
  const techSkills = [
    'JavaScript', 'Python', 'Java', 'C++', 'React', 'Angular', 'Vue', 
    'Node.js', 'Express', 'Django', 'Flask', 'Spring', 'SQL', 'NoSQL',
    'MongoDB', 'PostgreSQL', 'MySQL', 'AWS', 'Azure', 'GCP', 'Docker',
    'Kubernetes', 'CI/CD', 'Git', 'Machine Learning', 'Data Science',
    'AI', 'Deep Learning', 'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision'
  ];
  
  const softSkills = [
    '团队协作', '沟通', '领导力', '解决问题', '时间管理', '项目管理',
    '批判性思维', '创新', '适应性', '灵活性', '自我激励', '分析思维'
  ];
  
  const foundTechSkills = techSkills.filter(skill => 
    content.toLowerCase().includes(skill.toLowerCase())
  );
  
  const foundSoftSkills = softSkills.filter(skill => 
    content.toLowerCase().includes(skill.toLowerCase())
  );
  
  return {
    technical: foundTechSkills,
    soft: foundSoftSkills
  };
}

// 提取教育背景（示例）
function extractEducation(content: string) {
  // 简单示例，实际应用中应该使用更复杂的正则表达式或NLP
  const educationKeywords = ['大学', '学院', '学士', '硕士', '博士', 'MBA', '学位'];
  const hasEducation = educationKeywords.some(keyword => 
    content.includes(keyword)
  );
  
  return {
    detected: hasEducation,
    level: hasEducation ? '已检测到教育背景' : '未检测到教育背景',
    details: '需要更高级的分析来提取详细教育信息'
  };
}

// 提取工作经验（示例）
function extractExperience(content: string) {
  // 简单示例，实际应用中应该使用更复杂的正则表达式或NLP
  const experienceKeywords = ['经验', '工作', '职位', '项目', '负责', '开发', '管理', '实习'];
  const hasExperience = experienceKeywords.some(keyword => 
    content.includes(keyword)
  );
  
  return {
    detected: hasExperience,
    years: '需要更高级的分析来确定年限',
    details: '需要更高级的分析来提取详细工作经验'
  };
}

// 生成改进建议（示例）
function generateSuggestions(content: string, skills: any, experience: any) {
  const suggestions = [];
  
  // 检查内容长度
  if (content.length < 1000) {
    suggestions.push('简历内容较短，建议添加更多详细信息');
  }
  
  // 检查技能数量
  if (skills.technical.length < 5) {
    suggestions.push('技术技能较少，建议添加更多相关技能');
  }
  
  if (skills.soft.length < 3) {
    suggestions.push('软技能较少，建议添加更多软技能展示');
  }
  
  // 检查是否有量化成果
  if (!content.match(/\d+%|\d+次|\d+个/g)) {
    suggestions.push('缺少量化的成果描述，建议添加具体数字展示成就');
  }
  
  // 检查行动导向语言
  const actionVerbs = ['开发', '设计', '实现', '领导', '管理', '创建', '优化', '提高', '减少', '解决'];
  const hasActionVerbs = actionVerbs.some(verb => content.includes(verb));
  if (!hasActionVerbs) {
    suggestions.push('缺少行动导向的语言，建议使用更多动词开始成就描述');
  }
  
  return suggestions;
}

// 计算简历得分（示例）
function calculateResumeScore(skills: any, education: any, experience: any) {
  let score = 0;
  
  // 技能得分（最高40分）
  score += Math.min(skills.technical.length * 3, 30);
  score += Math.min(skills.soft.length * 2, 10);
  
  // 教育背景得分（最高30分）
  if (education.detected) {
    score += 30;
  }
  
  // 工作经验得分（最高30分）
  if (experience.detected) {
    score += 30;
  }
  
  return score;
}
