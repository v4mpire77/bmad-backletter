"use client"

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-[#0A2342] mb-2">Blackletter Systems</h1>
          <p className="text-gray-600">Old rules. New game.</p>
        </div>
        <div className="bg-white p-8 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-center">Login Coming Soon</h2>
          <p className="text-gray-600 text-center mb-6">
            Authentication features are planned for future releases.
          </p>
          <div className="text-center">
            <a 
              href="/" 
              className="inline-block bg-[#0A2342] text-white px-6 py-2 rounded-md hover:bg-[#0A2342]/90 transition-colors"
            >
              Go to Contract Review
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
