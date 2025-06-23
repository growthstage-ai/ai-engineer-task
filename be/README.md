# FastAPI Backend Setup (with uv)

This backend is a FastAPI application that exposes a simple "hello world" endpoint. It is designed to work with the Next.js frontend provided in the `chat/` directory.

---

## Prerequisites

- **Python 3.8+**
- **[uv](https://github.com/astral-sh/uv)** (for fast Python environment management)
  - Install with: `pip install uv`

---

## Setup Instructions

1. **Clone the repository and navigate to the backend directory:**

   ```bash
   cd python-server
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   uv venv .venv
   uv pip install -r requirements.txt
   ```

3. **Activate the virtual environment:**

   - On **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
   The server will start at [http://localhost:8000](http://localhost:8000).

---

## Database & Admin Utilities

- You generally do **not** need to edit the scripts in `admin_utils/` during normal operation.
- If you need to destroy and recreate the database, re-download manuals, and re-ingest all PDFs (for example, after schema changes or to reset the backend state), run:

  ```bash
  python admin_utils/setup.py
  ```

- For more details, see [`admin_utils/README.md`](./admin_utils/README.md).

---

## Environment Variables

- No environment variables are required for the default setup.
- If you add any, create a `.env` file in this directory and load them in `main.py` as needed.

---

## Troubleshooting

- **CORS errors:** Ensure both servers are running on the correct ports and the FastAPI CORS settings allow `http://localhost:3000`.
- **uv issues:** Make sure `uv` is installed and you are using a compatible Python version.
- **Port conflicts:** If ports 8000 or 3000 are in use, stop other processes or change the port in the server configs.

---

## License

MIT
