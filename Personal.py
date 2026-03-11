#################################################################################################
### COMP1811 - CW1 Outlook Simulator                                                          ###
###            Personal Class                                                                 ###
###            Handles personal emails with statistics generation and special display         ###
### Partner B:                                                                                ###
###            Hashir Shafiq, SID 001422142                              ###
#################################################################################################

from Mail import *
import re


class Personal(Mail):
    """Personal email class that inherits from Mail and adds text statistics"""

    def __init__(self, m_id, frm, to, date, subject, tag, body):
        super().__init__(m_id, frm, to, date, subject, tag, body)
        self._tag = "prsnl"
        self.add_stats()

    def add_stats(self):
        """
        Modifies email body:
        - Replaces 'Body' with sender's UID (text before @)
        - Appends statistics: word count, average word length, longest word length
        """
        # Extract UID from sender email
        uid = self._frm.split('@')[0] if '@' in self._frm else self._frm

        # Replace first occurrence of "Body" with UID
        modified_body = self._body.replace("Body", uid, 1)

        # Extract words for statistics (alphanumeric sequences)
        words = re.findall(r'\b[a-zA-Z0-9]+\b', modified_body)

        # Calculate statistics
        word_count = len(words)
        if word_count > 0:
            total_chars = sum(len(word) for word in words)
            avg_length = total_chars // word_count
            longest_length = max(len(word) for word in words)
        else:
            avg_length = 0
            longest_length = 0

        # Append statistics in exact specification format
        stats = f" Stats:Word count:{word_count}, Average word length:{avg_length}, Longest word length:{longest_length}."

        # Ensure body ends with period before adding stats
        if not modified_body.rstrip().endswith('.'):
            modified_body = modified_body.rstrip() + '.'

        self._body = modified_body + stats

    def show_email(self):
        """Display personal email in specification format"""
        print(f"From:{self._frm}")
        print(f"To:{self._to}")
        print(f"Date:{self._date}")
        print(f"Subject:{self._subject}")
        print(f"Tag:{self._tag}")
        print(f"Body:{self._body}")
        print(f"Read:{self._read}")
        print(f"Flagged:{self._flag}")

    @staticmethod
    def display_psnl(mailbox):
        """Display 'Persontology' and all personal emails sorted by date (newest first)"""
        print("\n" + "=" * 50)
        print("Persontology")
        print("=" * 50)

        # Filter personal emails
        personal_emails = [email for email in mailbox if isinstance(email, Personal)]

        # Sort by date in descending order (newest first)
        def parse_date(email):
            try:
                day, month, year = map(int, email.date.split('/'))
                return (year, month, day)
            except:
                return (0, 0, 0)

        sorted_emails = sorted(personal_emails, key=parse_date, reverse=True)

        for email in sorted_emails:
            email.show_email()