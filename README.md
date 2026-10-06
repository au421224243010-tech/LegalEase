# LegalEase — AI-Powered Legal Document Generator

Single-server FastAPI web application for AI-assisted legal document drafting with Google Gemini. The same FastAPI server serves the frontend, API, and document exports.

## Features
- Gemini-powered drafting
- Employment contracts, NDAs, leases, service agreements, offer letters and more
- Editable preview
- TXT, DOCX and PDF exports
- Optional logo upload for exported documents
- Responsive dark UI
- `/health` endpoint
- Render-ready production configuration

## Local setup
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and set:
```env
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
```
live site:
https://legalease-zuam.onrender.com/

## Render
Build: `pip install -r requirements.txt`
Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
Environment variables: `GEMINI_API_KEY`, `GEMINI_MODEL`.

## GitHub collaboration
Have the repository owner add your GitHub username as a collaborator. For a safer workflow, use a feature branch and Pull Request:
```bash
git checkout -b feature/legal-doc-generator
git add .
git commit -m "feat: initial LegalEase application"
git push -u origin feature/legal-doc-generator
```
Then open a Pull Request into `main`.

## Legal disclaimer
LegalEase generates AI-assisted drafts for educational and productivity purposes. It is not a law firm or substitute for qualified legal advice. Important documents should be reviewed by a qualified legal professional before signing or relying on them.
