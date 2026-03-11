#################################################################################################
### COMP1811 - CW1 Outlook Simulator                                                          ###
###            Mail Class                                                                     ###
###            Base class representing email messages with core attributes and display        ###
###            functionality, serving as parent for specialized email types                   ###
#
### Partner A:                                                                                ###
###            Bhavya Solanki, SID 001455161                                                  ###
### Partner B:                                                                                ###
###            Hashir Shafiq, SID 001422142                                                   ###
#################################################################################################

# DO NOT CHANGE CLASS OR METHOD NAMES
# replace "pass" with your own code as specified in the CW spec.

class Mail:
    """
    Base email class representing a general email message in the OutlookSim system.

    Stores core email attributes such as sender, recipient, subject, date, tag and body,
    along with read/flag status. This class provides the default implementation for
    displaying email details and acts as the parent class for specialised email types
    such as Confidential and Personal.
    """
    # DO NOT CHANGE CLASS OR METHOD NAMES
    def  __init__(self,m_id,frm,to,date,subject,tag,body):
        self._m_id = m_id
        self._frm = frm
        self._to = to
        self._subject = subject
        self._date = date
        self._tag = tag      # reference to Outlook mail folder email is stored in
                             # e.g. tag0 = inbox, tag1 = bin, tag2 = private, tag3 = bank_acct, tag4 = COMP1811, etc.
        self._body = body
        self._flag = False   # Boolean indicating whether email is important
        self._read = False   # Boolean indicating whether the email is read or not.
        self._signature = "" # Concept 3: Digital Signature for Integrity
        self._is_spam = False # Concept 4: Spam Detection Tag

    # Format should be done from pretty print.
    def __str__(self):
        return f"m_id:{self.m_id}\tfrom:{self.frm}\t|{self.to}\t|{self.date}|{self.subject}|{self.tag}|{self.read}|{self.flag}"

    @property
    def m_id(self):
        return self._m_id

    @property
    def frm(self):
        return self._frm

    @property
    def to(self):
        return self._to

    @property
    def date(self):
        return self._date

    @property
    def body(self):
        return self._body

    @property
    def subject(self):
        return self._subject

    @property
    def tag(self):
        return self._tag

    @property
    def read(self):
        return self._read

    @property
    def flag(self):
        return self._flag

    @tag.setter
    # Pre: value in tags.
    def tag(self, value):
        self._tag = value

    @read.setter
    def read(self,value):
        self._read = value

    @flag.setter
    def flag(self,value):
        self._flag = value

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, value):
        self._signature = value

    @property
    def is_spam(self):
        return self._is_spam

    @is_spam.setter
    def is_spam(self, value):
        self._is_spam = value

# FEATURES A (Partner A)
    # FA.2
    # Pretty display of email details
    def show_email(self):
        """Display email in formatted way as per specification"""
        print(f"From:{self._frm}")
        print(f"To:{self._to}")
        print(f"Date:{self._date}")
        print(f"Subject:{self._subject}")
        print(f"Tag:{self._tag}")
        print(f"Body:{self._body}")
        print(f"Read:{self._read}")
        print(f"Flagged:{self._flag}")