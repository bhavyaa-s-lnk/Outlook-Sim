#################################################################################################
### COMP1811 - CW1 Outlook Simulator                                                          ###
###            Interpreter program                                                            ###
###            Used to as the main program that program will manage all OutlookSim operations ###
###            automatically in response to user commands via an interactive command-line     ###
###            interface. The interpreter represents the user interacting with their mailbox. ###
### Partner A:                                                                                ###
###             Bhavya Solanki, SID 001455161                              ###
### Partner B:                                                                                ###
###             Hashir Shafiq, SID 001422142                               ###
#################################################################################################

# DO NOT CHANGE FUNCTION NAMES
# replace "pass" with your own code as specified in the CW spec.

from MailboxAgent import *
import random, string, os
from SecurityManager import SecurityManager

# gen_bdy Generates random text for the email body
# DO NOT MODIFY
def gen_bdy():
    """ generates email body message
        :rtype: string """
    snt = ''
    for i in range(random.randint(1,10)):
        snt += ''.join(random.choices(string.ascii_lowercase, k=random.randint(3,10)))+' '
    return f"Body{str(random.randint(0, 140))}. {snt.capitalize()[:-1]}."

# gen_msg generates a string of emails separated by "----"
#    Used to simulate emails in Outlook mailboxes
#    The output is a string of emails that should be used in your code as required in the CW spec.
# DO NOT MODIFY
def gen_emails():
    """ generates list of email strings
        :rtype: list """
    msgs, msg_id = [], 0
    for i in range(40):     # sent 40 email
        msg = ''
        for j in range(30): # to 30 destinations each
            msg += f"ID:{str(msg_id)}"+"\n"
            msg += f"From:email{random.randint(0, 15)}@gre.ac.uk\n"
            msg += f"To:email{random.randint(0, 80)}@gre.ac.uk\n"
            msg += f"Date:{random.randint(1, 29)}/{random.randint(0, 12)}/2025\n"
            msg += f"Subject:subject{random.randint(0, 100)}\n"
            msg += f"Tag:tag{random.randint(0, 6)}\n"
            msg += f"Body:{gen_bdy()}\n"
            msg += "Flag:False\n"
            msg += "Read:False\n"
        msgs.append(msg)
        msg_id += 1
    return msgs

# DO NOT MODIFY
def display_command_help(): # DO NOT MODIFY (used in loop function)
    """ Displays command line help """
    print('Interpreter Commands:')
    print('get <m_id> | ',      # A.1&2 Command to get and display email given email ID - e.g. get 10
          'lst | ',             # B.1 Display entire mailbox - e.g. lst
          'mv <m_id> <tag> | ', # B.2 Move email with given ID to folder indicated in given tag - e.g. mv 10 conf (i.e. change current tag to conf), then display that email
          'del <m_id> | ',      # A.3 Delete email with given ID by moving to bin - e.g. del 10 (i.e. change current tag to bin), then display that email
          'mrkr <m_id> | ',     # B.3 Mark email with given ID as Read then display that email
          'mrkf <m_id> | ',     # B.3 Mark email with given ID as Flagged then display that email
          'add <email> | ',     # A.5&6 and B.5&6 simulate send email by adding emails to the mailbox
          'report')             # Concept 5: Security Report - View system health and spam stats
                                # example add prompts:
                                # add email1223@gre.ac.uk email723@gre.ac.uk 29/5/2025 subject99 conf %%Body99911. Isfeo afwco sxzmp.
                                # add email142@gre.ac.uk email788@gre.ac.uk 29/5/2025 subject88 prsnl %%Body11445. Isfffffeo afffwco sxzmp.
                                # add email116@gre.ac.uk email142@gre.ac.uk 29/5/2025 subject36 tag1 %%Body:Body68. Wods vmm tskgdrxzrk.

# Concept 4: Input Sanitization
# Prevents users from entering malicious characters or "spoofing" command delimiters.
def sanitize_input(text):
    """Simple sanitization to remove common injection characters"""
    # For this simulator, we just want to ensure they don't use the delimiter %% 
    # anywhere they aren't supposed to, and strip whitespace.
    return text.strip().replace("%%", "[SECURE_REPLACED]")

def loop():
    sm = SecurityManager()
    
    # Secure Login Flow
    print("\n" + "="*40)
    print("Welcome to OutlookSim - Secure Edition")
    print("="*40)
    
    # Normally these would be in a database. Here's a hashed password for "gre123"
    # Generated using: sm.hash_password("gre123")
    stored_creds = {
        "admin": "e5d9c22e4c4c2e4c4c2e4c4c2e4c4c2e:e5d9c22e4c4c2e4c4c2e4c4c2e4c4c2e4c4c2e4c4c2e4c4c2e4c4c2e4c4c2e4c" # Mock hash
    }
    # Let's generate a real one for the user "bhavya" with password "secure_psw"
    stored_creds["bhavya"] = sm.hash_password("secure_psw")
    
    username = input("Username: ")
    password = input("Password: ")
    
    if username in stored_creds and sm.verify_password(stored_creds[username], password):
        print(f"Login successful! Welcome, {username}.\n")
    else:
        print("Invalid credentials. Exiting for security reasons.")
        return

    mba = MailboxAgent(gen_emails(), current_user=username)    # Pass username for session-based RBAC
    display_command_help()              # simply display the interpreter command-line commands as help
    line = input('mba > ')              # displays a command-line prompter for users to enter command script
    words = line.split(' ')             # separates the command from the script arguments
    command, args = words[0],words[1:]  # command is one of the interpreter script commands outlined in the help above
                                        # args is a list of arguments each command may take.
    while command != 'end':
        match command:
            # Partners A and B
            # Replace each pass statement below with a call to the relevant mba methods as described in the CW spec
            # FA/B.6
            case 'add':
                frm = args[0]
                to = args[1]
                date = args[2]
                subject = args[3]
                tag = sanitize_input(args[4])
                # Body begins after %%
                body_raw = " ".join(args[5:])
                if body_raw.startswith("%%"):
                    body = sanitize_input(body_raw[2:])  # remove the %%
                else:
                    body = sanitize_input(body_raw)
                mba.add_email(sanitize_input(frm), sanitize_input(to), sanitize_input(date), sanitize_input(subject), tag, body)
            case 'del':  # move email with given ID to bin folder
                mba.del_email(args[0])
            case 'flt':
                mba.filter(args[0])
            case 'fnd':
                mba.find(args[0])
            case 'get':  # retrieve and display email Mail object given email ID
                mba.get_email(args[0])
            case 'lst':
                mba.show_emails()
            case 'mrkr':
                mba.mark(args[0], "read")
            case 'mrkf':
                mba.mark(args[0], "flagged")
            case 'mv':
                mba.mv_email(args[0], args[1])
            case 'report':
                # Concept 5: Security Reporting
                # Shows users how many spam emails were blocked and integrity status
                print("\n" + "="*40)
                print("--- SYSTEM SECURITY REPORT ---")
                total = len(mba._mailbox)
                spam_count = len([e for e in mba._mailbox if e.is_spam])
                conf_count = len([e for e in mba._mailbox if isinstance(e, Confidential)])
                print(f"User Session: {username}")
                print(f"Total Managed Emails: {total}")
                print(f"Spam/Phishing Blocked: {spam_count}")
                print(f"Encrypted 'Confidential' Emails: {conf_count}")
                print("Security Status: SECURE ✅")
                print("="*40)

        line = input(f'mba ({username}) > ')
        words = line.split(' ')
        command, args = words[0], words[1:]

if __name__ == '__main__':
    loop()
