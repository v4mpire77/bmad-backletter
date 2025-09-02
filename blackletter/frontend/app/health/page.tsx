export default async function Page() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/healthz`, { cache: 'no-store' });
  const data = await res.json();
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
