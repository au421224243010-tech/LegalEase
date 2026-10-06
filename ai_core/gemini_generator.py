import os
import asyncio

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)


class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        ).strip()

        self.client = (
            genai.Client(api_key=self.api_key)
            if self.api_key
            else None
        )

    async def generate_document(
        self,
        document_type,
        parties,
        terms,
        effective_date,
        company_name=""
    ):
        if not self.client:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured on the server."
            )

        prompt = f"""
You are LegalEase, an AI legal-document drafting assistant.

Create a professional legal-document draft based only on the information
provided by the user.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

COMPANY / BRAND NAME:
{company_name or "Not provided"}

TERMS AND CONDITIONS:
{terms}

REQUIREMENTS:

1. Create a professional and well-structured legal-document draft.
2. Use a clear document title.
3. Use clear headings and numbered sections.
4. Include clauses appropriate to the selected document type.
5. Use the information supplied by the user accurately.
6. Do not invent laws, statutes, court cases, addresses, amounts, dates,
   personal information, or facts.
7. Use [PLACEHOLDER] for important missing information.
8. Include appropriate sections such as:
   - Introduction
   - Parties
   - Purpose
   - Terms and Conditions
   - Responsibilities
   - Confidentiality where applicable
   - Termination where applicable
   - Governing Law where applicable
   - Signatures
9. Make the document editable and easy to read.
10. Do not claim that the document is guaranteed to be legally valid
    or enforceable.
11. State that it is an AI-generated draft that should be reviewed by
    a qualified legal professional before use.
12. Return plain text only.
13. Do not use Markdown code fences.
14. Do not add explanations outside the document.

Generate the final legal-document draft now.
"""

        # Retry temporary Gemini 503/429 failures
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                text = getattr(response, "text", None)

                if not text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return text.strip()

            except Exception as exc:
                error_message = str(exc)

                is_temporary = (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                    or "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                )

                if is_temporary and attempt < max_attempts - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue

                raise RuntimeError(
                    f"Gemini generation failed using model "
                    f"'{self.model}': {error_message}"
                ) from exc