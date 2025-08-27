import { defineConfig } from "vitest/config";
import { fileURLToPath } from "url";

export default defineConfig({
  css: {
    // Avoid loading app's PostCSS/Tailwind config during tests
    postcss: null,
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./test/setup.ts"],
    include: ["test/**/*.test.{ts,tsx}"],
    css: false,
  },
});
