import AnalysisDetailClient from './AnalysisDetailClient';

interface AnalysisDetailPageProps {
  params: { jobId: string };
}

export default function AnalysisDetailPage({ params }: AnalysisDetailPageProps) {
  return <AnalysisDetailClient jobId={String(params.jobId)} />;
}

export async function generateStaticParams() {
  // In a real production build, you might fetch real job IDs here.
  // Providing a placeholder allows the static export build to succeed
  // while enabling dynamic, on-demand rendering during tests.
  return [{ jobId: 'placeholder' }];
}

