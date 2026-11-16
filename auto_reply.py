"""Compatibility wrapper for the auto-reply secretary agent."""

from auto_reply.email_tracker import EmailMessage, analyze_emails, build_reply, classify_email, parse_email_file

__all__ = [
    "EmailMessage",
    "analyze_emails",
    "build_reply",
    "classify_email",
    "parse_email_file",
]
