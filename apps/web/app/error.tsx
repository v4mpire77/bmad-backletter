"use client";
export default function Error({ error }: { error: Error }) {
  return (
    <div className="min-h-[40vh] grid place-items-center">
      <div className="text-center">
        <h1 className="text-xl font-semibold">Something went wrong</h1>
        <p className="text-neutral-600">{error.message}</p>
        <a href="/" className="underline mt-2 inline-block">Go home</a>
      </div>
    </div>
  );
}
