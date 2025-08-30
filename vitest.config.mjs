export default {
  test: {
    globals: true,
    coverage: { reporter: ["text", "lcov"], statements: 90, branches: 85 },
    include: ["automation/__tests__/**/*.test.js"],
    environment: "node",
    passWithNoTests: false
  }
};
