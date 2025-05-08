"use client";

import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

// 模拟的工作详情数据
const mockJobDetails = {
  1: {
    id: 1,
    title: '前端开发工程师',
    company: '科技有限公司',
    location: '北京',
    salary: '25k-35k',
    description: '我们正在寻找一位有经验的前端开发工程师加入我们的团队。您将负责开发和维护用户界面，确保网站的响应性和性能。',
    requirements: [
      '3年以上前端开发经验',
      '精通HTML、CSS和JavaScript',
      '熟悉React、Vue等前端框架',
      '良好的团队协作能力'
    ],
    benefits: [
      '有竞争力的薪资',
      '灵活的工作时间',
      '年度旅游',
      '健康保险'
    ]
  },
  2: {
    id: 2,
    title: '后端开发工程师',
    company: '互联网科技',
    location: '上海',
    salary: '30k-40k',
    description: '我们正在寻找一位后端开发工程师，负责设计、构建和维护高效、可扩展的服务器端应用程序。',
    requirements: [
      '5年以上后端开发经验',
      '精通Java、Python或Node.js',
      '熟悉数据库设计和优化',
      '了解微服务架构'
    ],
    benefits: [
      '有竞争力的薪资',
      '股票期权',
      '带薪休假',
      '职业发展机会'
    ]
  },
  // 其他工作详情...
  3: {
    id: 3,
    title: 'UI设计师',
    company: '创新科技',
    location: '深圳',
    salary: '20k-30k',
    description: '寻找有创意的UI设计师，负责创建美观且用户友好的界面设计。',
    requirements: [
      '3年以上UI设计经验',
      '精通Figma、Sketch等设计工具',
      '良好的色彩感知能力',
      '了解用户体验原则'
    ],
    benefits: [
      '有竞争力的薪资',
      '创意环境',
      '弹性工作',
      '专业发展机会'
    ]
  },
  4: {
    id: 4,
    title: '产品经理',
    company: '未来科技',
    location: '杭州',
    salary: '25k-35k',
    description: '寻找有经验的产品经理，负责产品的规划、开发和发布。',
    requirements: [
      '3年以上产品管理经验',
      '良好的沟通和协调能力',
      '数据分析能力',
      '了解软件开发流程'
    ],
    benefits: [
      '有竞争力的薪资',
      '职业发展路径',
      '团队建设活动',
      '健康保险'
    ]
  },
  5: {
    id: 5,
    title: '数据分析师',
    company: '数据科技',
    location: '广州',
    salary: '20k-30k',
    description: '寻找数据分析师，负责收集、处理和分析数据，提供业务洞察。',
    requirements: [
      '2年以上数据分析经验',
      '精通SQL和Excel',
      '熟悉数据可视化工具',
      '良好的沟通能力'
    ],
    benefits: [
      '有竞争力的薪资',
      '专业培训',
      '弹性工作时间',
      '年度奖金'
    ]
  }
};

export default function JobDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [jobDetail, setJobDetail] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 获取工作ID
    const jobId = params.id;
    
    // 模拟API请求
    setTimeout(() => {
      if (jobId && mockJobDetails[jobId as keyof typeof mockJobDetails]) {
        setJobDetail(mockJobDetails[jobId as keyof typeof mockJobDetails]);
      }
      setLoading(false);
    }, 500);
  }, [params.id]);

  const handleApply = () => {
    alert('申请功能即将上线，敬请期待！');
  };

  const handleBack = () => {
    router.back();
  };

  if (loading) {
    return (
      <main className="container mx-auto p-6">
        <div className="text-center py-10">
          <p>加载中...</p>
        </div>
      </main>
    );
  }

  if (!jobDetail) {
    return (
      <main className="container mx-auto p-6">
        <div className="text-center py-10">
          <h1 className="text-2xl font-bold mb-4">未找到工作信息</h1>
          <button 
            onClick={handleBack}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
          >
            返回搜索
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="container mx-auto p-6">
      <button 
        onClick={handleBack}
        className="mb-4 text-blue-500 hover:text-blue-700 flex items-center"
      >
        ← 返回搜索结果
      </button>
      
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="border-b pb-4 mb-4">
          <h1 className="text-3xl font-bold">{jobDetail.title}</h1>
          <p className="text-xl text-gray-700 mt-2">{jobDetail.company}</p>
          <div className="flex mt-2 text-gray-600">
            <p className="mr-4">{jobDetail.location}</p>
            <p>薪资: {jobDetail.salary}</p>
          </div>
        </div>
        
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">职位描述</h2>
          <p className="text-gray-700">{jobDetail.description}</p>
        </div>
        
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">要求</h2>
          <ul className="list-disc pl-5 text-gray-700">
            {jobDetail.requirements.map((req: string, index: number) => (
              <li key={index} className="mb-1">{req}</li>
            ))}
          </ul>
        </div>
        
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">福利</h2>
          <ul className="list-disc pl-5 text-gray-700">
            {jobDetail.benefits.map((benefit: string, index: number) => (
              <li key={index} className="mb-1">{benefit}</li>
            ))}
          </ul>
        </div>
        
        <div className="mt-8">
          <button 
            onClick={handleApply}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold"
          >
            申请职位
          </button>
        </div>
      </div>
    </main>
  );
}