#!/usr/bin/env python3
"""
Smart Email Sorter Agent CLI
A simple agentic app that automatically classifies and sorts emails
"""

import argparse
import sys
from email_agent import EmailAgent, EmailFolder

def main():
    parser = argparse.ArgumentParser(description="Smart Email Sorter Agent")
    parser.add_argument("--email-file", default="emails.json", 
                       help="Path to email JSON file (default: emails.json)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process and sort all emails")
    
    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show summary of unread emails")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List emails")
    list_parser.add_argument("--folder", choices=["inbox", "work", "personal", "spam", "promotional"],
                           help="Filter by folder")
    list_parser.add_argument("--unread", action="store_true", help="Show only unread emails")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show email statistics")
    
    # Read command
    read_parser = subparsers.add_parser("read", help="Mark email as read")
    read_parser.add_argument("email_id", type=int, help="Email ID to mark as read")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive mode")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize the email agent
    agent = EmailAgent(args.email_file)
    
    if args.command == "process":
        agent.process_emails()
    
    elif args.command == "summary":
        print(agent.summarize_unread_emails())
    
    elif args.command == "list":
        if args.folder:
            emails = agent.get_emails_by_folder(args.folder)
            print(f"\n📁 Emails in {args.folder.upper()} folder:")
        elif args.unread:
            emails = agent.get_unread_emails()
            print("\n📧 Unread emails:")
        else:
            emails = agent.emails
            print("\n📧 All emails:")
        
        if not emails:
            print("No emails found.")
        else:
            for email in emails:
                status = "📩" if not email.read else "📖"
                priority = "🔥" if email.priority == "high" else "📌" if email.priority == "normal" else "📝"
                category = f"[{email.category.upper()}]" if email.category else "[UNCATEGORIZED]"
                
                print(f"{status} {priority} ID:{email.id} - {category}")
                print(f"   From: {email.sender}")
                print(f"   Subject: {email.subject}")
                print(f"   Folder: {email.folder}")
                print(f"   Time: {email.timestamp}")
                print()
    
    elif args.command == "stats":
        stats = agent.get_stats()
        print("\n📊 Email Statistics:")
        print(f"Total emails: {stats['total_emails']}")
        print(f"Unread emails: {stats['unread_emails']}")
        
        print("\n📁 By Folder:")
        for folder, count in stats['folders'].items():
            print(f"  {folder}: {count}")
        
        if stats['categories']:
            print("\n🏷️  By Category:")
            for category, count in stats['categories'].items():
                print(f"  {category}: {count}")
    
    elif args.command == "read":
        if agent.mark_as_read(args.email_id):
            agent.save_emails()
            print(f"✅ Email {args.email_id} marked as read.")
        else:
            print(f"❌ Email {args.email_id} not found.")
    
    elif args.command == "interactive":
        interactive_mode(agent)

def interactive_mode(agent):
    """Interactive CLI mode"""
    print("\n🤖 Welcome to Smart Email Sorter Agent!")
    print("Type 'help' for available commands or 'quit' to exit.\n")
    
    while True:
        try:
            command = input("📧 > ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            elif command == 'help':
                print("\nAvailable commands:")
                print("  process    - Process and sort all emails")
                print("  summary    - Show summary of unread emails")
                print("  list       - List all emails")
                print("  unread     - List unread emails")
                print("  inbox      - Show inbox emails")
                print("  work       - Show work emails")
                print("  personal   - Show personal emails")
                print("  spam       - Show spam emails")
                print("  stats      - Show email statistics")
                print("  read <id>  - Mark email as read")
                print("  help       - Show this help")
                print("  quit       - Exit")
                print()
            
            elif command == 'process':
                agent.process_emails()
                print()
            
            elif command == 'summary':
                print(agent.summarize_unread_emails())
            
            elif command == 'list':
                print("\n📧 All emails:")
                for email in agent.emails:
                    status = "📩" if not email.read else "📖"
                    priority = "🔥" if email.priority == "high" else "📌"
                    print(f"{status} {priority} ID:{email.id} - {email.subject} ({email.sender})")
                print()
            
            elif command == 'unread':
                unread = agent.get_unread_emails()
                if unread:
                    print("\n📩 Unread emails:")
                    for email in unread:
                        priority = "🔥" if email.priority == "high" else "📌"
                        print(f"📩 {priority} ID:{email.id} - {email.subject} ({email.sender})")
                else:
                    print("No unread emails! 🎉")
                print()
            
            elif command in ['inbox', 'work', 'personal', 'spam', 'promotional']:
                emails = agent.get_emails_by_folder(command)
                if emails:
                    print(f"\n📁 {command.upper()} folder:")
                    for email in emails:
                        status = "📩" if not email.read else "📖"
                        priority = "🔥" if email.priority == "high" else "📌"
                        print(f"{status} {priority} ID:{email.id} - {email.subject} ({email.sender})")
                else:
                    print(f"No emails in {command} folder.")
                print()
            
            elif command == 'stats':
                stats = agent.get_stats()
                print("\n📊 Email Statistics:")
                print(f"Total: {stats['total_emails']}, Unread: {stats['unread_emails']}")
                print("Folders:", ", ".join([f"{k}:{v}" for k, v in stats['folders'].items()]))
                if stats['categories']:
                    print("Categories:", ", ".join([f"{k}:{v}" for k, v in stats['categories'].items()]))
                print()
            
            elif command.startswith('read '):
                try:
                    email_id = int(command.split()[1])
                    if agent.mark_as_read(email_id):
                        agent.save_emails()
                        print(f"✅ Email {email_id} marked as read.")
                    else:
                        print(f"❌ Email {email_id} not found.")
                except (IndexError, ValueError):
                    print("❌ Invalid command. Use: read <email_id>")
                print()
            
            else:
                print(f"❌ Unknown command: {command}")
                print("Type 'help' for available commands.")
                print()
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
