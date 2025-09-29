import unicodedata
import re
from difflib import SequenceMatcher

def normalize_text(text: str) -> str:
    if not text:
        return ""
    # Remove accents/diacritics
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    # Lowercase and strip whitespace
    return text.lower().strip()

def levenshtein_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def parse_name(name: str):
    parts = name.split()
    if len(parts) == 0:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[-1]

def parse_email(email: str):
    if '@' not in email:
        return email, ""
    prefix, domain = email.split('@', 1)
    return prefix, domain

def bird_heuristic(pair1, pair2):
    name1, email1 = pair1["name"], pair1["email"]
    name2, email2 = pair2["name"], pair2["email"]

    name1 = normalize_text(name1)
    name2 = normalize_text(name2)
    email1 = normalize_text(email1)
    email2 = normalize_text(email2)

    firstname1, lastname1 = parse_name(name1)
    firstname2, lastname2 = parse_name(name2)

    prefix1, domain1 = parse_email(email1)
    prefix2, domain2 = parse_email(email2)

    # C1: name similarity
    c1 = levenshtein_similarity(name1, name2)
    c2 = levenshtein_similarity(prefix1, prefix2)
    c3_1 = levenshtein_similarity(firstname1, firstname2)
    c3_2 = levenshtein_similarity(lastname1, lastname2)

    # C4-C7: check initials + lastname/firstname containment
    c4 = c5 = c6 = c7 = False
    if firstname1 and lastname1:
        c4 = (firstname1[0] in prefix2) and (lastname1 in prefix2)
    if lastname1:
        c5 = (lastname1[0] in prefix2) and (firstname1 in prefix2)
    if firstname2 and lastname2:
        c6 = (firstname2[0] in prefix1) and (lastname2 in prefix1)
    if lastname2:
        c7 = (lastname2[0] in prefix1) and (firstname2 in prefix1)

    return {
        "name_1" : name1,
        "email_1" : email1,
        "name_2" : name2,
        "email_2" : email2,
        "c1" :c1,
        "c2" : c2,
        "c3.1" : c3_1,
        "c3.2" : c3_2,
        "c4" : c4,
        "c5" : c5,
        "c6" : c6,
        "c7" : c7,
    }

if __name__ == "__main__":
    # Example usage
    pairs = [
        ("John Doe", "jdoe@example.com"),
        ("J. Doe", "john.doe@example.com"),
        ("Jane Smith", "jsmith@example.com"),
        ("J Smyth", "j.smyth@example.com"),
    ]

    for i in range(len(pairs)):
        for j in range(i+1, len(pairs)):
            if bird_heuristic(pairs[i], pairs[j], threshold=0.8):
                print(f"Duplicate detected: {pairs[i]} <-> {pairs[j]}")
