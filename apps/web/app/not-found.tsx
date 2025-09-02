export default function NotFound() {
  return (
    <div className="min-h-[40vh] grid place-items-center">
      <div className="text-center">
        <h1 className="text-xl font-semibold">Page not found</h1>
        <p className="text-neutral-600">Try the <a className="underline" href="/">home page</a>.</p>
      </div>
    </div>
  );
}
