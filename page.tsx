"use client";

import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
          智能求职助手
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          集改简历、写自荐信、搜工作和投简历为一体的智能系统，帮助您高效找到理想工作
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link
            href="/resume"
            className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            开始使用
          </Link>
          <Link
            href="#features"
            className="px-6 py-3 bg-gray-200 text-gray-800 font-medium rounded-lg hover:bg-gray-300 transition-colors"
          >
            了解更多
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-12">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          主要功能
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">简历管理</h3>
            <p className="text-gray-600">
              上传和分析您的简历，获取专业的改进建议，突出关键技能和成就，提高简历质量
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">工作搜索</h3>
            <p className="text-gray-600">
              从LinkedIn、Indeed和Glassdoor等多个招聘网站搜索工作机会，支持多种过滤条件
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">工作匹配</h3>
            <p className="text-gray-600">
              智能匹配算法分析您的简历与工作机会的匹配度，帮助您找到最适合的职位
            </p>
          </div>

          {/* Feature 4 */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">自荐信生成</h3>
            <p className="text-gray-600">
              根据您的简历和目标职位自动生成个性化自荐信，支持多种风格模板
            </p>
          </div>

          {/* Feature 5 */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">自动申请</h3>
            <p className="text-gray-600">
              自动填表和提交简历到招聘网站，跟踪申请状态，提高求职效率
            </p>
          </div>

          {/* Feature 6 */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">数据分析</h3>
            <p className="text-gray-600">
              提供详细的工作搜索报告、匹配分析和申请状态统计，帮助您优化求职策略
            </p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-12 bg-gray-50 rounded-xl p-8">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          使用流程
        </h2>
        <div className="max-w-4xl mx-auto">
          <div className="relative">
            {/* Steps */}
            <div className="flex flex-col md:flex-row md:items-center mb-8">
              <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-blue-600 text-white font-bold text-xl z-10">
                1
              </div>
              <div className="md:ml-6 mt-4 md:mt-0">
                <h3 className="text-xl font-semibold">上传简历</h3>
                <p className="text-gray-600 mt-2">
                  上传您的简历文件，系统会自动分析内容并提供改进建议
                </p>
              </div>
            </div>

            <div className="flex flex-col md:flex-row md:items-center mb-8">
              <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-blue-600 text-white font-bold text-xl z-10">
                2
              </div>
              <div className="md:ml-6 mt-4 md:mt-0">
                <h3 className="text-xl font-semibold">搜索工作</h3>
                <p className="text-gray-600 mt-2">
                  设置搜索条件，从多个招聘网站搜索工作机会
                </p>
              </div>
            </div>

            <div className="flex flex-col md:flex-row md:items-center mb-8">
              <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-blue-600 text-white font-bold text-xl z-10">
                3
              </div>
              <div className="md:ml-6 mt-4 md:mt-0">
                <h3 className="text-xl font-semibold">匹配工作</h3>
                <p className="text-gray-600 mt-2">
                  系统自动分析简历与工作的匹配度，找出最适合您的职位
                </p>
              </div>
            </div>

            <div className="flex flex-col md:flex-row md:items-center mb-8">
              <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-blue-600 text-white font-bold text-xl z-10">
                4
              </div>
              <div className="md:ml-6 mt-4 md:mt-0">
                <h3 className="text-xl font-semibold">生成自荐信</h3>
                <p className="text-gray-600 mt-2">
                  为目标职位自动生成个性化自荐信，提高申请成功率
                </p>
              </div>
            </div>

            <div className="flex flex-col md:flex-row md:items-center">
              <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-blue-600 text-white font-bold text-xl z-10">
                5
              </div>
              <div className="md:ml-6 mt-4 md:mt-0">
                <h3 className="text-xl font-semibold">自动申请</h3>
                <p className="text-gray-600 mt-2">
                  一键自动申请多个职位，跟踪申请状态，提高求职效率
                </p>
              </div>
            </div>

            {/* Vertical line */}
            <div className="absolute top-0 left-6 h-full w-0.5 bg-gray-200 -z-10 hidden md:block"></div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">
          准备好开始您的求职之旅了吗？
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          立即使用智能求职助手，让您的求职过程更高效、更成功
        </p>
        <Link
          href="/resume"
          className="px-8 py-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors text-lg"
        >
          立即开始
        </Link>
      </section>
    </div>
  );
}
