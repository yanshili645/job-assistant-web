import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-white text-xl font-bold">
          Job Assistant
        </Link>
        <div className="space-x-4">
          <Link href="/" className="text-white hover:text-gray-300">
            Home
          </Link>
          <Link href="/resume" className="text-white hover:text-gray-300">
            Resume
          </Link>
          <Link href="/jobs" className="text-white hover:text-gray-300">
            Jobs
          </Link>
          <Link href="/interview" className="text-white hover:text-gray-300">
            Interview
          </Link>
        </div>
      </div>
    </nav>
  );
}