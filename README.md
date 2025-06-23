# AI Engineer Project

This repository contains both the backend and frontend code for the project. The codebase is organized into two main directories:

- [`be/`](./be/): Backend (Python)
- [`fe/`](./fe/): Frontend (Next.js/React)

## Getting Started

**Important:**  
Before running any backend or frontend code, make sure you are in the correct directory:

- For backend tasks, `cd` into the `be/` directory.
- For frontend tasks, `cd` into the `fe/` directory.

Each subproject has its own README with setup and usage instructions.

---

## Large Files & Git LFS

**Note:**  
This repository uses [Git LFS](https://git-lfs.github.com/) to store large files (such as databases, binaries, and PDFs) in the `be/` directory.  
**You must install Git LFS before cloning or pulling the repository** to ensure all files are downloaded correctly.

### How to Install and Use Git LFS

1. **Install Git LFS**  
   Download from [git-lfs.github.com](https://git-lfs.github.com/) or use your package manager:

   ```bash
   # Windows (Chocolatey)
   choco install git-lfs

   # macOS (Homebrew)
   brew install git-lfs

   # Linux (Debian/Ubuntu)
   sudo apt-get install git-lfs
   ```

2. **Initialize Git LFS in your repo (first time only):**

   ```bash
   git lfs install
   ```

3. **Clone the repository as usual:**
   ```bash
   git clone <repo-url>
   ```

If you add new large files (e.g., `.db`, `.bin`, `.pdf`), track them with:

```bash
git lfs track "*.db"
git lfs track "*.bin"
git lfs track "*.pdf"
git lfs track "*.sqlite3"
git add .gitattributes
git add <your-large-file>
git commit -m "Track large files with Git LFS"
git push
```

For more details, see the [Git LFS documentation](https://git-lfs.github.com/).

---

## Project Structure

```
.
├── be/         # Backend code (Python)
│   ├── admin_utils/      # Admin scripts and utilities
│   ├── chroma_db/        # ChromaDB database files
│   ├── pdfs/             # PDF documents for ingestion
│   ├── main.py           # Main backend entry point
│   ├── requirements.txt  # Python dependencies
│   └── README.md         # Backend instructions
├── fe/         # Frontend code (Next.js/React)
│   ├── public/           # Static assets
│   ├── src/              # Frontend source code
│   ├── package.json      # Frontend dependencies
│   └── README.md         # Frontend instructions
└── README.md   # (This file)
```

---

## Backend

- **Directory:** [`be/`](./be/)
- **Language:** Python
- **Instructions:** See [`be/README.md`](./be/README.md)

**Tip:**  
Always `cd be/` before running backend scripts or installing Python dependencies.

---

## Frontend

- **Directory:** [`fe/`](./fe/)
- **Framework:** Next.js (React, TypeScript)
- **Instructions:** See [`fe/README.md`](./fe/README.md)

**Tip:**  
Always `cd fe/` before running frontend scripts or installing Node dependencies.

---

## Additional Notes

- Each subproject is self-contained. Follow the instructions in the respective README files for setup, development, and deployment.
- If you encounter issues, check the subproject README first for troubleshooting steps.
