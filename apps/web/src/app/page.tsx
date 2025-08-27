import { redirect } from "next/navigation";

export default function Home() {
  // Default to landing page; dashboard remains at /dashboard
  redirect("/landing");
}
