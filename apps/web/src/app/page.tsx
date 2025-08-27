import { redirect } from "next/navigation";

export default function Home() {
  // Default to dashboard per story guidance; landing remains at /landing
  redirect("/dashboard");
}
