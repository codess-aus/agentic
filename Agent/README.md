# Smart Email Sorter Agent 🤖📧

A simple but powerful agentic app that automatically classifies and sorts emails using rule-based intelligence.

## Features

- **Automatic Email Classification**: Categorizes emails into Work, Personal, Spam, and Promotional
- **Smart Folder Organization**: Automatically moves emails to appropriate folders
- **Priority Detection**: Identifies high-priority emails that need attention
- **Email Summarization**: Provides intelligent summaries of unread emails
- **Interactive CLI**: Easy-to-use command-line interface
- **Real-time Processing**: Processes emails and saves changes automatically

## Installation

1. Navigate to the Agent directory:
```bash
cd Agent
```

2. No external dependencies required! The agent uses only Python standard library.

## Quick Start

### 1. Process All Emails
Automatically classify and sort all emails in your inbox:
```bash
python cli.py process
```

### 2. Get Email Summary
See a smart summary of your unread emails:
```bash
python cli.py summary
```

### 3. Interactive Mode
Start the interactive CLI for ongoing email management:
```bash
python cli.py interactive
```

## Command Reference

### Basic Commands
- `python cli.py process` - Process and sort all emails
- `python cli.py summary` - Show summary of unread emails
- `python cli.py stats` - Show email statistics
- `python cli.py interactive` - Start interactive mode

### List Commands
- `python cli.py list` - List all emails
- `python cli.py list --unread` - List only unread emails
- `python cli.py list --folder inbox` - List emails in specific folder

### Email Management
- `python cli.py read <email_id>` - Mark an email as read

## Interactive Mode Commands

Once in interactive mode, you can use these commands:
- `process` - Process and sort emails
- `summary` - Show unread email summary
- `list` - List all emails
- `unread` - Show unread emails
- `inbox/work/personal/spam` - Show emails in specific folder
- `stats` - Show statistics
- `read <id>` - Mark email as read
- `help` - Show help
- `quit` - Exit

## How It Works

### Email Classification
The agent uses intelligent rule-based classification:

**Work Emails** - Detected by:
- Keywords: project, deadline, meeting, report, team, etc.
- Domains: company.com, work.com, corp.com
- Content: business-related language

**Personal Emails** - Detected by:
- Keywords: family, friend, dinner, weekend, etc.
- Domains: family.com, friend.com, personal.com
- Content: casual, personal language

**Spam Emails** - Detected by:
- Keywords: urgent, winner, lottery, million, etc.
- Suspicious phrases: "click here", "limited time"
- Known spam domains

**Promotional Emails** - Detected by:
- Keywords: sale, discount, deal, newsletter
- Commercial language patterns

### Agent Workflow
1. **Perception**: Reads emails from JSON data source
2. **Reasoning**: Analyzes content using classification rules
3. **Action**: Sorts emails into appropriate folders
4. **Learning**: Maintains statistics and provides insights

## Email Data Format

The agent works with JSON email data:
```json
{
  "id": 1,
  "sender": "boss@company.com",
  "subject": "Project Update",
  "body": "Email content...",
  "timestamp": "2025-05-28T09:30:00Z",
  "folder": "inbox",
  "read": false,
  "priority": "high"
}
```

## Example Usage

### Process emails and see results:
```bash
$ python cli.py process
🤖 Email Agent is processing your emails...
Classified 6 emails.
Sorted 6 emails into folders.
✅ Processing complete! Classified 6 and sorted 6 emails.

⚠️  You have 1 high priority unread emails!
   • Q4 Project Deadline - Important from boss@company.com
```

### Get a summary:
```bash
$ python cli.py summary
You have 6 unread emails:

📁 WORK (2 emails):
  • From: boss@company.com
    Subject: Q4 Project Deadline - Important
    Priority: high

  • From: hr@company.com
    Subject: Employee Benefits Update
    Priority: normal

📁 PERSONAL (2 emails):
  • From: mom@family.com
    Subject: Sunday Dinner Plans
    Priority: normal
...
```

## Extending the Agent

### Add LLM Classification
Replace rule-based classification with AI:
```python
# Add to requirements.txt: openai>=1.0.0
import openai

class LLMClassifier:
    def classify(self, email):
        # Use OpenAI API for classification
        pass
```

### Add Email Fetching
Connect to real email servers:
```python
# Add to requirements.txt: imaplib, smtplib
import imaplib

class EmailFetcher:
    def fetch_emails(self):
        # Connect to IMAP server
        pass
```

### Add Notifications
Send alerts for high-priority emails:
```python
# Add desktop notifications or Slack integration
```

## Architecture

```
📁 Agent/
├── 📄 emails.json          # Email data storage
├── 🐍 email_agent.py       # Core agent logic
├── 🐍 cli.py              # Command-line interface
├── 📄 requirements.txt     # Dependencies
└── 📄 README.md           # This file
```

## Contributing

Feel free to extend this agent with:
- LLM-based classification
- Real email server integration
- Web interface
- Mobile notifications
- Advanced filtering rules
- Email templates and auto-replies

This is a great starting point for building more sophisticated agentic applications!
