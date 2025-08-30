import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Auth from "@/components/Auth";

describe("Auth", () => {
  test("sign in button shows loading state", async () => {
    const signInWithOAuth = jest.fn().mockResolvedValue(undefined);
    const signOut = jest.fn().mockResolvedValue(undefined);
    render(<Auth signInWithOAuth={signInWithOAuth} signOut={signOut} />);

    const signInBtn = screen.getByRole("button", { name: /sign in/i });
    fireEvent.click(signInBtn);

    expect(signInBtn).toBeDisabled();
    expect(signInBtn).toHaveTextContent("Signing in...");

    await waitFor(() => expect(signInWithOAuth).toHaveBeenCalled());

    expect(signInBtn).not.toBeDisabled();
    expect(signInBtn).toHaveTextContent("Sign in");
  });

  test("sign out button shows loading state", async () => {
    const signInWithOAuth = jest.fn().mockResolvedValue(undefined);
    const signOut = jest.fn().mockResolvedValue(undefined);
    render(<Auth signInWithOAuth={signInWithOAuth} signOut={signOut} />);

    const signOutBtn = screen.getByRole("button", { name: /sign out/i });
    fireEvent.click(signOutBtn);

    expect(signOutBtn).toBeDisabled();
    expect(signOutBtn).toHaveTextContent("Signing out...");

    await waitFor(() => expect(signOut).toHaveBeenCalled());

    expect(signOutBtn).not.toBeDisabled();
    expect(signOutBtn).toHaveTextContent("Sign out");
  });
});
