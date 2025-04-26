// 部署前准备脚本

// 这个脚本用于在部署前准备环境，包括安装依赖、构建应用和初始化数据库

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 确保目录存在
function ensureDirectoryExists(directory) {
  if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
    console.log(`创建目录: ${directory}`);
  }
}

// 执行命令并打印输出
function runCommand(command, cwd = process.cwd()) {
  console.log(`执行命令: ${command}`);
  try {
    const output = execSync(command, { cwd, stdio: 'inherit' });
    return output;
  } catch (error) {
    console.error(`命令执行失败: ${error.message}`);
    process.exit(1);
  }
}

// 主函数
async function main() {
  console.log('开始部署准备...');
  
  // 确保migrations目录存在
  ensureDirectoryExists(path.join(process.cwd(), 'migrations'));
  
  // 安装依赖
  console.log('安装依赖...');
  runCommand('npm install');
  
  // 安装Wrangler（如果需要）
  console.log('安装Wrangler...');
  runCommand('npm install -g wrangler');
  
  // 初始化本地数据库
  console.log('初始化本地数据库...');
  try {
    runCommand('wrangler d1 create job_assistant_db --local');
  } catch (error) {
    console.log('数据库可能已存在，继续执行...');
  }
  
  // 应用数据库迁移
  console.log('应用数据库迁移...');
  runCommand('wrangler d1 execute job_assistant_db --local --file=migrations/0001_initial.sql');
  
  // 构建应用
  console.log('构建应用...');
  runCommand('npm run build');
  
  console.log('部署准备完成！');
  console.log('现在可以使用以下命令启动开发服务器:');
  console.log('npm run dev');
  console.log('或者使用以下命令部署到Cloudflare:');
  console.log('wrangler deploy');
}

// 执行主函数
main().catch(error => {
  console.error('部署准备失败:', error);
  process.exit(1);
});
