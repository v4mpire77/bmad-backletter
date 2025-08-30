import { useState } from "react";

interface AuthProps {
  signInWithOAuth: () => Promise<unknown>;
  signOut: () => Promise<unknown>;
}

export default function Auth({ signInWithOAuth, signOut }: AuthProps) {
  const [loading, setLoading] = useState(false);
  const [action, setAction] = useState<"signin" | "signout" | null>(null);

  const handleSignIn = async () => {
    setLoading(true);
    setAction("signin");
    try {
      await signInWithOAuth();
    } finally {
      setLoading(false);
      setAction(null);
    }
  };

  const handleSignOut = async () => {
    setLoading(true);
    setAction("signout");
    try {
      await signOut();
    } finally {
      setLoading(false);
      setAction(null);
    }
  };

  return (
    <div className="flex gap-2">
      <button
        onClick={handleSignIn}
        disabled={loading && action === "signin"}
        className="rounded bg-black px-4 py-2 text-white disabled:opacity-50"
      >
        {loading && action === "signin" ? "Signing in..." : "Sign in"}
      </button>
      <button
        onClick={handleSignOut}
        disabled={loading && action === "signout"}
        className="rounded bg-gray-200 px-4 py-2 disabled:opacity-50"
      >
        {loading && action === "signout" ? "Signing out..." : "Sign out"}
      </button>
    </div>
  );
}
