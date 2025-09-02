import AnalysesClient from './AnalysesClient';

export async function generateStaticParams() {
  // Replace with your logic to fetch all analysis ids
  return [{ id: 'mock-id-123' }];
}

export default function AnalysesPage({
  params,
}: {
  params: { id: string };
}) {
  return <AnalysesClient id={params.id} />;
}
