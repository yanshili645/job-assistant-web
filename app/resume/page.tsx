"use client";

import { useState } from 'react';

export default function ResumePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };
  
  const handleUpload = () => {
    if (!selectedFile) {
      alert('请先选择文件');
      return;
    }
    
    // 这里可以添加实际的上传逻辑，例如使用API发送文件到服务器
    alert(`文件 "${selectedFile.name}" 上传成功！（模拟）`);
    setSelectedFile(null);
    
    // 重置文件输入框
    const fileInput = document.getElementById('resume-file') as HTMLInputElement;
    if (fileInput) fileInput.value = '';
  };

  return (
    <main className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">简历管理</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <p className="mb-4">在这里上传和管理您的简历。</p>
        <div className="mb-4">
          <h2 className="text-xl font-semibold mb-2">我的简历</h2>
          <div className="border border-gray-200 rounded p-4 mb-4">
            <p className="text-gray-500">暂无上传的简历。</p>
          </div>
        </div>
        
        <div className="mb-4">
          <label htmlFor="resume-file" className="block mb-2">选择文件：</label>
          <input 
            type="file" 
            id="resume-file" 
            accept=".pdf,.doc,.docx" 
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded file:border-0
                      file:text-sm file:font-semibold
                      file:bg-blue-50 file:text-blue-700
                      hover:file:bg-blue-100"
          />
          {selectedFile && (
            <p className="mt-2 text-sm text-gray-600">已选择: {selectedFile.name}</p>
          )}
        </div>
        
        <button 
          onClick={handleUpload}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          上传简历
        </button>
      </div>
    </main>
  );
}