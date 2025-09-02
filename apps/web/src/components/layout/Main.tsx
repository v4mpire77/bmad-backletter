export default function Main({ children }: { children: React.ReactNode }) {
  return (
    <main id="main-content" className="flex-1 px-4 py-6 md:px-6">
      {children}
    </main>
  );
}

