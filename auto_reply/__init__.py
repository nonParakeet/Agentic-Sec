"""Email tracking and auto-reply utilities for the secretary agent."""

from .email_tracker import EmailMessage, build_reply, classify_email

__all__ = ["EmailMessage", "build_reply", "classify_email"]
