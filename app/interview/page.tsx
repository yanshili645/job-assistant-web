export default function InterviewPage() {
  return (
    <main className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Interview Preparation</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <p className="mb-4">Prepare for your interviews with practice questions and tips.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-100 p-4 rounded">
            <h2 className="text-xl font-semibold mb-2">Practice Questions</h2>
            <p>Access common interview questions for your field.</p>
          </div>
          <div className="bg-gray-100 p-4 rounded">
            <h2 className="text-xl font-semibold mb-2">Mock Interviews</h2>
            <p>Schedule a mock interview with AI assistance.</p>
          </div>
        </div>
      </div>
    </main>
  );
}