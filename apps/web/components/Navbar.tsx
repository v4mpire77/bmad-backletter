export default function Navbar() {
  return (
    <nav className="border-b bg-white/80 backdrop-blur">
      <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between">
        <a href="/" className="font-medium">Blackletter</a>
        <div className="flex gap-4 text-sm">
          <a href="/upload" className="hover:underline">Upload</a>
          <a href="/analyses/demo" className="hover:underline">Findings</a>
          <a href="#" className="opacity-40 pointer-events-none">History</a>
          <a href="#" className="opacity-40 pointer-events-none">Settings</a>
        </div>
      </div>
    </nav>
  );
}
