import GrievanceDetailClient from "./GrievanceDetailClient";

export default async function AdminGrievanceDetailPage({ params }) {
  const { id } = await params;

  return <GrievanceDetailClient />;
}

