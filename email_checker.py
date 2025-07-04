
import smtplib
import dns.resolver
import socket

def check_email_smtp(email):
    domain = email.split('@')[1]

    # Get MX record
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange).rstrip('.')
    except Exception as e:
        return False  # No MX record found

    # Try SMTP handshake
    try:
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_record)
        server.helo("example.com")  # Use your domain here
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()

        return code in [250, 251]
    except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, socket.timeout, socket.gaierror):
        return False

def generate_emails(first_name, last_name, domain):
    first = first_name.lower()
    last = last_name.lower()
    f = first[0]
    l = last[0]

    patterns = set([
        f"{first}@{domain}",
        f"{last}@{domain}",
        f"{first}.{last}@{domain}",
        f"{f}.{last}@{domain}",
        f"{first}.{l}@{domain}",
        f"{f}{last}@{domain}",
        f"{first}{last}@{domain}",
        f"{first}_{last}@{domain}",
        f"{f}_{last}@{domain}",
        f"{first}-{last}@{domain}",
        f"{first}{l}@{domain}",
        f"{last}{f}@{domain}",
        f"{last}.{f}@{domain}",
        f"{last}_{f}@{domain}",
        f"{last}-{f}@{domain}",
        f"{l}.{first}@{domain}",
        f"{f}@{domain}",
        f"{f}{l}@{domain}",
        f"{f}.{l}@{domain}",
        f"{f}_{l}@{domain}",
        f"{f}-{l}@{domain}",
        f"{first}{l}@{domain}",
        f"{f}{last}@{domain}",
        f"{first}{last[0]}@{domain}",
        f"{first[0]}{last[0]}@{domain}",
        f"{first[0]}{last}@{domain}",
        f"{last[0]}{first}@{domain}",
        f"{last[0]}{first[0]}@{domain}",
    ])

    results = {}
    for email in sorted(patterns):
        is_valid = check_email_smtp(email)
        results[email] = "Valid" if is_valid else "Invalid"
    return results
