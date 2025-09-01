# Developer Quick Start

This guide helps new developers get the Blackletter framework running locally in minutes.

## Prerequisites

- Windows 11 with Developer Mode enabled or a recent Linux/macOS release
- Docker Desktop
- Git
- Node.js 20+
- Python 3.11
- Tesseract OCR (`choco install tesseract` on Windows)
- Optional: [Ollama](https://ollama.ai) for local LLM support

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/blackletter-systems.git
   cd blackletter-systems
   ```

2. **Run the startup script**
   - Windows:
     ```powershell
     .\start.ps1
     ```
   - Linux/macOS:
     ```bash
     ./start.sh
     ```

   The script creates a `.env` file, installs dependencies, and starts Docker containers, the backend API, and the frontend.

3. **Verify services**
   - Frontend: <http://localhost:3000>
   - Backend API: <http://localhost:8000>
   - API docs: <http://localhost:8000/docs>
   - MinIO Console: <http://localhost:9001>
   - n8n automation: <http://localhost:5678>

4. **Run tests**
   ```bash
   pytest
   ```

5. **Try the interactive example**
   ```bash
   python examples/upload_and_review.py path/to/contract.pdf
   ```
   The script uploads a document, waits for processing, and prints a summary.

## Next Steps

- Review the [API documentation](../API_DOCUMENTATION.md)
- Explore the `examples` and `templates` directories for more guidance
- Check `docs/TEAM_ONBOARDING_CHECKLIST.md` to complete setup
