import os

from dotenv import load_dotenv
from google import genai


# Load variables from .env
# override=True ensures the values in your local .env are used.
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
        # Check API key
        if not self.client:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured on the server."
            )

        # Check model
        if not self.model:
            raise RuntimeError(
                "GEMINI_MODEL is not configured."
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

6. Do not invent:
   - laws
   - statutes
   - court cases
   - addresses
   - monetary amounts
   - personal information
   - dates
   - facts

7. If important information is missing, use:
   [PLACEHOLDER]

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

11. This is an AI-generated draft and should be reviewed by a qualified
    legal professional before use.

12. Return plain text only.

13. Do not use Markdown code fences.

14. Do not add explanations outside the document.

Generate the final legal-document draft now.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

        except Exception as exc:
            error_message = str(exc)

            raise RuntimeError(
                f"Gemini generation failed using model "
                f"'{self.model}': {error_message}"
            ) from exc

        # Extract generated text
        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()