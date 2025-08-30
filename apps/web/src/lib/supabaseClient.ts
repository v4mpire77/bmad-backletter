import { createClient } from "@supabase/supabase-js";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!url || !anonKey) {
  const missing = [] as string[];
  if (!url) missing.push("NEXT_PUBLIC_SUPABASE_URL");
  if (!anonKey) missing.push("NEXT_PUBLIC_SUPABASE_ANON_KEY");
  const message = `Missing Supabase environment variables: ${missing.join(", ")}`;
  console.warn(message);
  throw new Error(message);
}

export const supabase = url && anonKey ? createClient(url, anonKey) : undefined;
