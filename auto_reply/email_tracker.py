from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

CATEGORY_PATTERNS = {
    "no_reply": [
        r"\bno[- ]?reply\b",
        r"\bdo not reply\b",
        r"\bthis email is automated\b",
        r"\bauto[- ]?reply\b",
    ],
    "unsubscribe": [
        r"\bunsubscribe\b",
        r"\bopt[- ]?out\b",
        r"\bremove me from this list\b",
        r"\bstop receiving emails\b",
    ],
    "spam": [
        r"\bspam\b",
        r"\bjunk\b",
        r"\bscam\b",
        r"\bfree money\b",
        r"\bclaim your prize\b",
        r"\bviagra\b",
        r"\bclick here\b",
        r"\bwin a prize\b",
    ],
}


def _normalize_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value).strip().lower()


@dataclass
class EmailMessage:
    sender: str = ""
    subject: str = ""
    body: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_text(cls, raw_email: str) -> "EmailMessage":
        if not raw_email:
            return cls()

        sender = ""
        subject = ""
        body_lines: List[str] = []
        current_section = "body"

        for line in raw_email.splitlines():
            if not line.strip():
                if current_section == "body":
                    continue
                current_section = "body"
                continue

            if re.match(r"(?i)^from:\s*", line):
                sender = line.split(":", 1)[1].strip()
                current_section = "header"
                continue
            if re.match(r"(?i)^subject:\s*", line):
                subject = line.split(":", 1)[1].strip()
                current_section = "header"
                continue
            if current_section == "body":
                body_lines.append(line.strip())

        body = "\n".join(part for part in body_lines if part)

        if not sender:
            match = re.search(r"(?im)^from:\s*(.+)$", raw_email)
            if match:
                sender = match.group(1).strip()

        if not subject:
            match = re.search(r"(?im)^subject:\s*(.+)$", raw_email)
            if match:
                subject = match.group(1).strip()

        if not body:
            body = re.sub(r"(?im)^from:.*\n?", "", raw_email)
            body = re.sub(r"(?im)^subject:.*\n?", "", body)
            body = re.sub(r"\n{3,}", "\n\n", body).strip()

        return cls(sender=sender, subject=subject, body=body)

    def summary(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "subject": self.subject,
            "category": classify_email(self.body or self.subject),
            "body_preview": (self.body or self.subject)[:180],
        }


def classify_email(email_or_text: str) -> str:
    if email_or_text is None:
        return "unknown"

    text = _normalize_text(email_or_text)
    if not text:
        return "unknown"

    for category, patterns in CATEGORY_PATTERNS.items():
        if any(re.search(pattern, text) for pattern in patterns):
            return category

    return "needs_response"


def _response_text(category: str) -> str:
    responses = {
        "no_reply": (
            "This message appears to be an automated notification or a no-reply address. "
            "No direct response is needed unless a support contact is explicitly provided."
        ),
        "unsubscribe": (
            "This looks like a subscription or bulk mailing. The best next step is to "
            "use the unsubscribe link, or mark it as irrelevant if you no longer want to receive it."
        ),
        "spam": (
            "This email appears to be spam or junk. Do not respond. Mark it as spam and move it to the junk folder."
        ),
        "needs_response": (
            "Thanks for reaching out. I will review this message and respond as needed."
        ),
        "unknown": (
            "I could not confidently classify this message. Please review it manually before replying."
        ),
    }
    return responses.get(category, responses["needs_response"])


def build_reply(email_or_text: str) -> Dict[str, Any]:
    if not email_or_text:
        return {"category": "unknown", "suggested_reply": _response_text("unknown")}

    if isinstance(email_or_text, EmailMessage):
        text = f"{email_or_text.subject}\n{email_or_text.body}"
    else:
        text = str(email_or_text)

    category = classify_email(text)
    reply = _response_text(category)
    return {"category": category, "suggested_reply": reply}


def parse_email_file(path: str) -> EmailMessage:
    with open(path, "r", encoding="utf-8") as handle:
        return EmailMessage.from_text(handle.read())


def analyze_emails(emails: Iterable[str]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for email in emails:
        msg = EmailMessage.from_text(email)
        result = msg.summary()
        result["auto_reply"] = build_reply(email)["suggested_reply"]
        results.append(result)
    return results


if __name__ == "__main__":
    sample = """From: newsletter@company.com
Subject: Weekly update

We are excited to bring you our latest features.
Unsubscribe here if you no longer wish to receive our updates.
"""
    print(json.dumps(build_reply(sample), indent=2))
