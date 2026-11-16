"""Project wrapper for the secretary mail tracker agent."""

from auto_reply.email_tracker import EmailMessage, build_reply, classify_email

__all__ = ["EmailMessage", "build_reply", "classify_email"]
