from __future__ import annotations

import argparse
import json
import sys

from auto_reply.email_tracker import build_reply, parse_email_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze email content and suggest an auto-reply.")
    parser.add_argument("input", nargs="?", help="Email text or a path to an email file.")
    parser.add_argument("--input", dest="message_flag", help="Email text to analyze.")
    parser.add_argument("--message", dest="message_flag_2", help="Email text to analyze.")
    parser.add_argument("--file", dest="file_path", help="Path to a file containing an email.")
    args = parser.parse_args()

    raw_message = args.message_flag or args.message_flag_2 or args.input

    if args.file_path:
        message = parse_email_file(args.file_path)
        email_body = f"{message.subject}\n{message.body}"
        payload = {
            "sender": message.sender,
            "subject": message.subject,
            "category": build_reply(email_body)["category"],
            "suggested_reply": build_reply(email_body)["suggested_reply"],
        }
        print(json.dumps(payload, indent=2))
        return 0

    if raw_message:
        payload = build_reply(raw_message)
        print(json.dumps(payload, indent=2))
        return 0

    data = sys.stdin.read()
    if data.strip():
        payload = build_reply(data)
        print(json.dumps(payload, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
