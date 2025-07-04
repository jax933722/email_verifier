import smtplib
import dns.resolver

def generate_patterns(first, last, domain):
    return [
        f"{first}.{last}@{domain}",
        f"{first[0]}.{last}@{domain}",
        f"{first}{last}@{domain}",
        f"{first}@{domain}",
        f"{first[0]}{last}@{domain}",
        f"{first}_{last}@{domain}"
    ]

def check_mx(domain):
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False

def validate_email(email):
    try:
        domain = email.split('@')[1]
        server = smtplib.SMTP(timeout=10)
        server.connect(f"smtp.{domain}")
        server.helo("test.com")
        server.mail("test@test.com")
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except:
        return False

def check_email_permutations(first, last, domain):
    first, last, domain = first.lower(), last.lower(), domain.lower()
    if not check_mx(domain):
        return {"error": "Domain has no MX records."}

    results = {}
    for email in generate_patterns(first, last, domain):
        valid = validate_email(email)
        results[email] = "Valid" if valid else "Invalid"
    return results
