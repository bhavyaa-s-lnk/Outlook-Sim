#################################################################################################
### COMP1811 - CW1 Outlook Simulator                                                          ###
###            Confidential Class                                                             ###
###            Specialized email subclass that handles confidential emails with automatic     ###
###            encryption functionality and secure display formatting                         ###
### Partner A:                                                                                ###
###            Bhavya Solanki, SID 001455161                                                  ###
#################################################################################################

from Mail import *
from SecurityManager import SecurityManager


class Confidential(Mail):
    """Confidential email class with automatic encryption functionality."""

    def __init__(self, m_id, frm, to, date, subject, tag, body, key="SECRET"):
        super().__init__(m_id, frm, to, date, subject, tag, body)
        self._tag = "conf"
        self._encryption_key = key
        self.encrypt()

    def encrypt(self):
        """
        Concept 2: Using SecurityManager's Vigenère Cipher.
        This replaces the basic letter-shifting with a key-based approach.
        """
        self._body = SecurityManager.vigenere_encrypt(self._body, self._encryption_key)
        # Sign the encrypted message to ensure integrity
        self._signature = SecurityManager.sign_message(self._body, self._encryption_key)

    def decrypt(self, key):
        """Allows authorized users to decrypt the message."""
        return SecurityManager.vigenere_decrypt(self._body, key)

    def show_email(self):
        """Display confidential email with integrity verification"""
        print("\n" + "*"*10 + " SECURE CONFIDENTIAL " + "*"*10)
        print(f"From: {self._frm}")
        print(f"Date: {self._date}")
        print(f"Subject: {self._subject}")
        print(f"Encrypted Body: {self._body}")
        
        # Verify integrity
        is_valid = SecurityManager.verify_signature(self._body, self._signature, self._encryption_key)
        status = "VALID ✅" if is_valid else "TAMPERED ❌"
        print(f"Integrity Status: {status}")
        print(f"Signature: {self._signature}")
        print("*"*41)

    @staticmethod
    def display_conf(mailbox):
        """Display all confidential emails sorted by sender"""
        print("\n" + "=" * 50)
        print("Smurfiology encrypted")
        print("=" * 50)

        # Filter confidential emails
        conf_emails = [email for email in mailbox if isinstance(email, Confidential)]

        # Sort by sender
        sorted_emails = sorted(conf_emails, key=lambda email: email.frm.lower())

        for email in sorted_emails:
            email.show_email()