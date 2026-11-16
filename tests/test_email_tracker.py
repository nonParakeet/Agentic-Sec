import unittest

from auto_reply.email_tracker import EmailMessage, build_reply, classify_email


class EmailTrackerTests(unittest.TestCase):
    def test_no_reply_detection(self):
        sample = """From: noreply@shop.com
Subject: Order update

This email is automated. Do not reply.
"""
        self.assertEqual(classify_email(sample), "no_reply")
        self.assertIn("No direct response", build_reply(sample)["suggested_reply"])

    def test_unsubscribe_detection(self):
        sample = """From: updates@newsletter.com
Subject: Weekly digest

Click here to unsubscribe if you'd like to stop receiving emails.
"""
        self.assertEqual(classify_email(sample), "unsubscribe")

    def test_spam_detection(self):
        sample = """From: winner@scam.xyz
Subject: Claim your prize!

You have won a free money prize. Click here now.
"""
        self.assertEqual(classify_email(sample), "spam")

    def test_parse_email_message(self):
        email = EmailMessage.from_text("From: help@example.com\nSubject: Hello\n\nCan you help me?")
        self.assertEqual(email.sender, "help@example.com")
        self.assertEqual(email.subject, "Hello")
        self.assertIn("help me", email.body.lower())


if __name__ == "__main__":
    unittest.main()
