import AnalysesClient from './AnalysesClient';

export async function generateStaticParams() {
  // Replace with your logic to fetch all jobIds
  return [{ jobId: 'mock-job-123' }];
}

export default function AnalysesPage({
  params,
}: {
  params: { jobId: string };
}) {
  return <AnalysesClient jobId={params.jobId} />;
}
