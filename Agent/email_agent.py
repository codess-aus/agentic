import json
import re
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class EmailCategory(Enum):
    WORK = "work"
    PERSONAL = "personal"
    SPAM = "spam"
    PROMOTIONAL = "promotional"

class EmailFolder(Enum):
    INBOX = "inbox"
    WORK = "work"
    PERSONAL = "personal"
    SPAM = "spam"
    PROMOTIONAL = "promotional"

@dataclass
class Email:
    id: int
    sender: str
    subject: str
    body: str
    timestamp: str
    folder: str
    read: bool
    priority: str
    category: str = None

class EmailClassifier:
    """Simple rule-based email classifier"""
    
    def __init__(self):
        # Work-related keywords and domains
        self.work_keywords = [
            'project', 'deadline', 'meeting', 'report', 'quarterly', 'budget',
            'team', 'colleague', 'office', 'employee', 'hr', 'benefits'
        ]
        self.work_domains = ['company.com', 'work.com', 'corp.com']
        
        # Spam indicators
        self.spam_keywords = [
            'urgent', 'winner', 'congratulations', 'lottery', 'million',
            'click here', 'limited time', 'act now', 'free money'
        ]
        self.spam_domains = ['spamsite.com', 'scam.com', 'fake.com']
        
        # Promotional keywords
        self.promo_keywords = [
            'sale', 'discount', '% off', 'deal', 'offer', 'newsletter',
            'unsubscribe', 'promotion', 'limited time'
        ]
        
        # Personal indicators
        self.personal_keywords = [
            'family', 'friend', 'dinner', 'weekend', 'personal', 'mom', 'dad',
            'sister', 'brother', 'hiking', 'vacation'
        ]
        self.personal_domains = ['family.com', 'friend.com', 'personal.com']
    
    def classify(self, email: Email) -> EmailCategory:
        """Classify email based on content and sender"""
        text = f"{email.subject} {email.body} {email.sender}".lower()
        
        # Check for spam first
        if any(keyword in text for keyword in self.spam_keywords) or \
           any(domain in email.sender for domain in self.spam_domains):
            return EmailCategory.SPAM
        
        # Check for promotional emails
        if any(keyword in text for keyword in self.promo_keywords):
            return EmailCategory.PROMOTIONAL
        
        # Check for work emails
        if any(keyword in text for keyword in self.work_keywords) or \
           any(domain in email.sender for domain in self.work_domains):
            return EmailCategory.WORK
        
        # Check for personal emails
        if any(keyword in text for keyword in self.personal_keywords) or \
           any(domain in email.sender for domain in self.personal_domains):
            return EmailCategory.PERSONAL
        
        # Default to personal if uncertain
        return EmailCategory.PERSONAL

class EmailAgent:
    """Smart Email Sorter Agent"""
    
    def __init__(self, email_file: str = "emails.json"):
        self.email_file = email_file
        self.classifier = EmailClassifier()
        self.emails = []
        self.load_emails()
    
    def load_emails(self):
        """Load emails from JSON file"""
        try:
            with open(self.email_file, 'r') as f:
                email_data = json.load(f)
                self.emails = [Email(**email) for email in email_data]
        except FileNotFoundError:
            print(f"Email file {self.email_file} not found. Starting with empty inbox.")
            self.emails = []
        except json.JSONDecodeError:
            print(f"Error reading {self.email_file}. Invalid JSON format.")
            self.emails = []
    
    def save_emails(self):
        """Save emails back to JSON file"""
        email_data = []
        for email in self.emails:
            email_dict = {
                'id': email.id,
                'sender': email.sender,
                'subject': email.subject,
                'body': email.body,
                'timestamp': email.timestamp,
                'folder': email.folder,
                'read': email.read,
                'priority': email.priority
            }
            if email.category:
                email_dict['category'] = email.category
            email_data.append(email_dict)
        
        with open(self.email_file, 'w') as f:
            json.dump(email_data, f, indent=2)
    
    def classify_all_emails(self):
        """Classify all unclassified emails"""
        classified_count = 0
        for email in self.emails:
            if not email.category:
                category = self.classifier.classify(email)
                email.category = category.value
                classified_count += 1
        
        print(f"Classified {classified_count} emails.")
        return classified_count
    
    def auto_sort_emails(self):
        """Automatically sort emails into folders based on classification"""
        sorted_count = 0
        for email in self.emails:
            if email.folder == "inbox" and email.category:
                # Move email to appropriate folder
                if email.category == EmailCategory.WORK.value:
                    email.folder = EmailFolder.WORK.value
                elif email.category == EmailCategory.PERSONAL.value:
                    email.folder = EmailFolder.PERSONAL.value
                elif email.category == EmailCategory.SPAM.value:
                    email.folder = EmailFolder.SPAM.value
                elif email.category == EmailCategory.PROMOTIONAL.value:
                    email.folder = EmailFolder.PROMOTIONAL.value
                
                sorted_count += 1
        
        print(f"Sorted {sorted_count} emails into folders.")
        return sorted_count
    
    def get_emails_by_folder(self, folder: str) -> List[Email]:
        """Get all emails in a specific folder"""
        return [email for email in self.emails if email.folder == folder]
    
    def get_unread_emails(self) -> List[Email]:
        """Get all unread emails"""
        return [email for email in self.emails if not email.read]
    
    def mark_as_read(self, email_id: int):
        """Mark an email as read"""
        for email in self.emails:
            if email.id == email_id:
                email.read = True
                return True
        return False
    
    def summarize_unread_emails(self) -> str:
        """Generate a summary of unread emails"""
        unread = self.get_unread_emails()
        if not unread:
            return "No unread emails."
        
        summary = f"You have {len(unread)} unread emails:\n\n"
        
        # Group by category
        categories = {}
        for email in unread:
            cat = email.category or "uncategorized"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(email)
        
        for category, emails in categories.items():
            summary += f"📁 {category.upper()} ({len(emails)} emails):\n"
            for email in emails[:3]:  # Show first 3 emails per category
                summary += f"  • From: {email.sender}\n"
                summary += f"    Subject: {email.subject}\n"
                summary += f"    Priority: {email.priority}\n\n"
            
            if len(emails) > 3:
                summary += f"  ... and {len(emails) - 3} more emails\n\n"
        
        return summary
    
    def get_high_priority_emails(self) -> List[Email]:
        """Get high priority unread emails"""
        return [email for email in self.emails 
                if email.priority == "high" and not email.read]
    
    def process_emails(self):
        """Main agent processing: classify and sort emails"""
        print("🤖 Email Agent is processing your emails...")
        
        # Step 1: Classify emails
        classified = self.classify_all_emails()
        
        # Step 2: Auto-sort emails
        sorted_count = self.auto_sort_emails()
        
        # Step 3: Save changes
        self.save_emails()
        
        print(f"✅ Processing complete! Classified {classified} and sorted {sorted_count} emails.")
        
        # Step 4: Alert about high priority emails
        high_priority = self.get_high_priority_emails()
        if high_priority:
            print(f"\n⚠️  You have {len(high_priority)} high priority unread emails!")
            for email in high_priority:
                print(f"   • {email.subject} from {email.sender}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get email statistics"""
        total = len(self.emails)
        unread = len(self.get_unread_emails())
        
        folders = {}
        categories = {}
        
        for email in self.emails:
            # Count by folder
            folders[email.folder] = folders.get(email.folder, 0) + 1
            # Count by category
            if email.category:
                categories[email.category] = categories.get(email.category, 0) + 1
        
        return {
            'total_emails': total,
            'unread_emails': unread,
            'folders': folders,
            'categories': categories
        }
