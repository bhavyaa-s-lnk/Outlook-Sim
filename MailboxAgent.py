#################################################################################################
### COMP1811 - CW1 Outlook Simulator                                                          ###
###            MailboxAgent Class                                                             ###
###            Central management system controlling mailbox operations including email       ###
###            retrieval, deletion, filtering, sorting, marking, and creation of all types    ###
     ###
### Partner A:                                                                                ###
###            Bhavya Solanki, SID 001455161                                                  ###
### Partner B:                                                                                ###
###            Hashir Shafiq, SID 001422142                              ###
#################################################################################################

# DO NOT CHANGE CLASS OR METHOD NAMES
# replace "pass" with your own code as specified in the CW spec.

from Mail import *
from Confidential import *
from Personal import *
from SecurityManager import SecurityManager

class MailboxAgent:
    """
        Central controller class responsible for managing all mailbox operations
        within the OutlookSim system.

        The MailboxAgent acts as the main processing unit that stores all Mail,
        Confidential, and Personal objects, and provides functionality for:

        - Generating the mailbox from raw email data
        - Retrieving individual emails by ID
        - Displaying single or multiple emails
        - Deleting emails by moving them to the 'bin' folder
        - Filtering emails by sender address
        - Sorting emails (by date or sender)
        - Marking emails as read or flagged
        - Finding emails by date
        - Creating and inserting new email objects (Mail, Confidential, Personal)
          depending on the folder tag

        This class integrates all features from both partners (A and B) and represents
        the central interface that the interpreter interacts with to simulate Outlook-like
        email behaviour using object-oriented programming.
        """
    def __init__(self, email_data, current_user="admin"): # Default to admin for compatibility
        self._mailbox = self.__gen_mailbox(email_data)
        self._current_user = current_user
        self._roles = {"admin": "all", "user": "own"} # Simple RBAC mapping

    # Given email_data (string containing each email on a separate line),
    # __gen_mailbox returns mailbox as a list containing received emails as Mail objects
    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, value):
        self._current_user = value

    @classmethod
    def __gen_mailbox(cls, email_data):
        """ generates mailbox data structure with security defaults """
        mailbox = []
        for e in email_data:
            msg = e.split('\n')
            # Extract fields safely
            try:
                m_id = msg[0].split(":")[1]
                frm = msg[1].split(":")[1]
                to = msg[2].split(":")[1]
                date = msg[3].split(":")[1]
                subject = msg[4].split(":")[1]
                tag = msg[5].split(":")[1]
                body = msg[6].split(":")[1]
                
                # Create object based on tag
                if tag == "conf":
                    mail_obj = Confidential(m_id, frm, to, date, subject, tag, body)
                elif tag == "prsnl":
                    mail_obj = Personal(m_id, frm, to, date, subject, tag, body)
                else:
                    mail_obj = Mail(m_id, frm, to, date, subject, tag, body)
                
                # Concept 3: Sign for integrity
                mail_obj.signature = SecurityManager.sign_message(mail_obj.body, "GLOBAL_KEY")
                # Concept 4: Spam Detection
                cls.spam_check(mail_obj)
                
                mailbox.append(mail_obj)
            except Exception:
                pass # Skip malformed records
        return mailbox

    @staticmethod
    def spam_check(mail_obj):
        """Heuristic-based spam detection"""
        spam_keywords = ["prize", "win", "urgent", "lottery", "inherit", "verify", "account", "money"]
        content = (mail_obj.subject + " " + mail_obj.body).lower()
        
        for word in spam_keywords:
            if word in content:
                mail_obj.is_spam = True
                if mail_obj.tag not in ["bin", "spam"]:
                    mail_obj.tag = "spam"
                return True
        return False

# FEATURES A (Partner A)
    # FA.1
    # Return Mail object with given ID
    def get_email(self, m_id):
        for mail in self._mailbox:
            if mail.m_id == m_id:
                mail.show_email()
                return mail
        print(f"Email ID {m_id} not found.")
        return None

    # FA.3
    # Move E-mail to bin
    def del_email(self, m_id):
        """Delete email by moving to bin folder"""
        for mail in self._mailbox:
            if mail.m_id == m_id:
                mail.tag = "bin"
                mail.show_email()
                return mail
        print(f"Email ID {m_id} not found.")
        return None

    # FA.4
    # Display emails from specific sender
    def filter(self, frm):
        """Filter and display emails from given sender"""
        found = False
        for mail in self._mailbox:
            if frm in mail.frm:
                mail.show_email()
                found = True
        if not found:
            print(f"No emails found from: {frm}")

    # FA.5
    # 
    def sort_date(self):
        """Sort mailbox by date (DD/MM/YYYY)"""

        def parse_date(d):
            day, month, year = d.split('/')
            return int(year), int(month), int(day)

        self._mailbox.sort(key=lambda mail: parse_date(mail.date))


# FEATURES B (Partner B)
    # FB.1
    # 
    def show_emails(self):
        """
        Display emails that the current user is authorized to see.
        Concept: Access Control Filtering.
        """
        visible_emails = []
        is_admin = self._current_user == "admin"
        
        for email in self._mailbox:
            # Users see emails sent TO them or FROM them. Admins see all.
            if is_admin or self._current_user in email.to or self._current_user in email.frm:
                visible_emails.append(email)

        if not visible_emails:
            print(f"No authorized emails found for user: {self._current_user}")
            return

        print(f"=== MAILBOX CONTENTS FOR {self._current_user.upper()} ===")
        for email in visible_emails:
            email.show_email()

    # FB.2
    # 
    def mv_email(self, m_id, tag):
        """Move email to a new tag/folder"""
        for email in self._mailbox:
            if email.m_id == m_id:
                email.tag = tag
                email.show_email()
                return email
        print(f"Email ID {m_id} not found.")
        return None

    # FB.3
    # 
    def mark(self, m_id, m_type):
        """Mark email as 'read' or 'flagged'"""
        for email in self._mailbox:
            if email.m_id == m_id:
                if m_type.lower() == "read":
                    email.read = True
                elif m_type.lower() == "flagged":
                    email.flag = True
                email.show_email()
                return email
        print(f"Email ID {m_id} not found.")
        return None

    # FB.4
    # 
    def find(self, date):
        """Find and return emails matching a specific date"""
        result = []
        for email in self._mailbox:
            if email.date.strip() == date.strip():
                email.show_email()
                result.append(email)
        if not result:
            print(f"No emails found for date: {date}")
        return result

    # FB.5
    # Sort by sender
    def sort_from(self):
        """Sort mailbox by sender email address"""
        self._mailbox.sort(key=lambda e: e.frm.lower())
        return self._mailbox



    # FEATURE 6 (Partners A and B)
    # Add new email
    def add_email(self, frm, to, date, subject, tag, body):
        """Add new email to mailbox based on tag type"""
        # Generate unique ID
        max_id = -1
        for e in self._mailbox:
            try:
                i = int(e.m_id)
                if i > max_id:
                    max_id = i
            except:
                pass

        new_id = str(max_id + 1)

        match tag.lower():

                # FA.6
                # Confidential email
                case 'conf':
                    new_email = Confidential(new_id, frm, to, date, subject, tag, body)
                    self._mailbox.append(new_email)
                    new_email.show_email()
                    return new_email
                # FB.6
                # Personal email
                case 'prsnl':
                    new_email = Personal(new_id, frm, to, date, subject, tag, body)
                    self._mailbox.append(new_email)
                    new_email.show_email()
                    return new_email
                # FA&B.6
                # Regular email
                case _:
                    new_email = Mail(new_id, frm, to, date, subject, tag, body)
                    new_email.signature = SecurityManager.sign_message(body, "GLOBAL_KEY")
                    self.spam_check(new_email)
                    self._mailbox.append(new_email)
                    new_email.show_email()
                    return new_email