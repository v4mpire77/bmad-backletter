import Link from 'next/link';

export default function Home() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Hello, world!</h1>
      <Link href="/admin" className="text-blue-600 underline">
        Admin
      </Link>
    </div>
  );
}
