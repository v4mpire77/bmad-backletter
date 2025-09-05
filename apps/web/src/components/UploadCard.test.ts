import { validateFile, MAX_FILE_SIZE } from "./UploadCard";

describe("validateFile", () => {
  it("rejects unsupported file types", () => {
    const file = new File(["data"], "test.txt", { type: "text/plain" });
    expect(validateFile(file)).toMatch(/only pdf or docx/i);
  });

  it("rejects oversized files", () => {
    const bigData = new Uint8Array(MAX_FILE_SIZE + 1);
    const file = new File([bigData], "big.pdf", { type: "application/pdf" });
    expect(validateFile(file)).toMatch(/10mb or less/i);
  });

  it("accepts valid files", () => {
    const file = new File(["data"], "ok.pdf", { type: "application/pdf" });
    expect(validateFile(file)).toBeNull();
  });
});
