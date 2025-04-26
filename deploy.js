// 部署脚本

// 这个脚本用于将应用部署到Cloudflare Pages

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

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
  console.log('开始部署应用...');
  
  // 运行部署准备脚本
  console.log('运行部署准备脚本...');
  runCommand('node deploy-prep.js');
  
  // 部署到Cloudflare
  console.log('部署到Cloudflare...');
  runCommand('wrangler deploy');
  
  console.log('部署完成！');
  console.log('您的应用现在已经部署到Cloudflare，可以通过以下URL访问:');
  console.log('https://job-assistant-web.pages.dev');
}

// 执行主函数
main().catch(error => {
  console.error('部署失败:', error);
  process.exit(1);
});
