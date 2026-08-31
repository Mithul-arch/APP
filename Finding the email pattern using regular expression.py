import re

EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
def find_emails(text):
    """Return all email-like substrings found anywhere in text."""
    return re.findall(EMAIL_PATTERN, text)

def is_valid_email(candidate):
    """Return True only if the ENTIRE string is a valid email (fullmatch)."""
    return re.fullmatch(EMAIL_PATTERN, candidate) is not None

if __name__ == "__main__":
    sample_text = """
    Hi team,

    Please reach out to rohan.sharma@example.com for onboarding questions,
    or cc priya_iyer99@company.co.in on the thread.
    For billing, contact billing+support@desi-shop.io before Friday.
    Do NOT use the old address admin@old_domain (it's broken),
    and note that not-an-email or www.example.com are not addresses.
    Our bot report also lists ananya.verma@sub.example.org as a backup contact.
    """

    print("STEP 1: find_emails() on sample_text")
    found = find_emails(sample_text)
    for i, email in enumerate(found, start=1):
        print(f"  {i}. {email}")
    print(f"\nTotal emails found: {len(found)}")

    print()
    print("STEP 2: is_valid_email() on individual test strings")

    test_cases = [
        ("rohan.sharma@example.com", True),
        ("priya_iyer99@company.co.in", True),
        ("billing+support@desi-shop.io", True),
        ("plainaddress", False),
        ("@missinglocal.com", False),
        ("missingatsign.com", False),
        ("user@.com", False),
        ("user@domain", False),
        ("user@domain..com", False),
        ("user@123.456.com", True),
    ]

    for candidate, expected in test_cases:
        actual = is_valid_email(candidate)
        result = "VALID" if actual else "INVALID"
        match_flag = "OK" if actual == expected else "MISMATCH vs expectation"
        print(f"  {candidate!r:35} -> {result:8} (expected valid={expected}) [{match_flag}]")