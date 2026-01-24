import GrievanceDetailClient from "./GrievanceDetailClient";

export default async function Page({ params }) {
  const { id } = await params;

  return <GrievanceDetailClient id={id} />;
}
