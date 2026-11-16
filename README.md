# Secretary Email Tracker

A small Python command-line tool that examines email text, classifies it, and
prints a suggested response as JSON. It uses simple keyword and phrase matching
and Python's standard library; no third-party packages or API keys are required.

## What it can do

The tracker recognizes these categories:

- `no_reply` — automated or no-reply messages
- `unsubscribe` — mailing-list messages with unsubscribe or opt-out language
- `spam` — messages containing common spam or junk indicators
- `needs_response` — other non-empty messages
- `unknown` — empty input that cannot be classified

It outputs the category and a suggested response. Treat the result as a draft:
review the message and suggestion yourself before taking action.

## What it does not do

The program does not connect to an email account, monitor an inbox, unsubscribe
you, move or delete messages, or send replies. It only analyzes text that you
provide and prints a suggestion.

## Requirements

- Python 3. dataclasses are used, so Python 3.7 or later is required.
- No additional dependencies.

Check that Python 3 is available:

```bash
python3 --version
```

## Run from the project folder

Open a terminal, change to the directory containing `main.py`, and run one of
the commands below. If the project is elsewhere, replace the example path with
its location.

### Analyze text directly

```bash
python3 main.py --input "Please unsubscribe me from these emails."
```

`--message` and a positional argument are also accepted:

```bash
python3 main.py --message "This email is automated. Do not reply."
python3 main.py "You have won free money. Click here."
```

### Analyze an email saved in a text file

Create a UTF-8 text file such as `sample_email.txt`:

```text
From: newsletter@example.com
Subject: Weekly update

Please unsubscribe if you no longer want to receive these emails.
```

Then run:

```bash
python3 main.py --file sample_email.txt
```

The file reader recognizes `From:` and `Subject:` headers. It includes the
sender and subject in the output when using `--file`.

### Pipe email text through standard input

```bash
cat sample_email.txt | python3 main.py
```

You can also paste or type text into `python3 main.py`, then press `Ctrl+D` on
Linux/macOS (or `Ctrl+Z`, then Enter, on Windows) to finish input.

## Output

Results are printed as JSON. For example:

```json
{
  "category": "unsubscribe",
  "suggested_reply": "This looks like a subscription or bulk mailing. ..."
}
```

## Run the tests

From the project folder:

```bash
python3 -m unittest discover -s tests -v
```

## Project entry points

- `main.py` — command-line entry point
- `auto_reply/cli.py` — command-line argument and input handling
- `auto_reply/email_tracker.py` — email parsing, classification, and reply suggestions
- `tests/test_email_tracker.py` — automated tests
