import unicodedata
import re
from Levenshtein import ratio as sim
import string

def preprocess_text(name: str) -> str:
    if not name:
        return ""
    trans = name.maketrans("", "", string.punctuation)
    name = name.translate(trans)
    name = unicodedata.normalize('NFKD', name)
    name = ''.join([c for c in name if not unicodedata.combining(c)])
    name = name.casefold()
    name = " ".join(name.split())
    return name

def get_first_last_name(name: str):
    parts = name.split(" ")
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) == 1:
        return name, ""
    else:
        return parts[0], " ".join(parts[1:])

def get_firt_index_value(first: str, last: str):
    i_first = first[0] if len(first) > 1 else ""
    i_last = last[0] if len(last) > 1 else ""
    return i_first, i_last

def calculate_similarity(a: str, b: str) -> float:
    return sim(a, b)

# Function for pre-processing each name,email
def process(dev):
    name: str = dev[0]
    name = preprocess_text(name)
    first, last = get_first_last_name(name)
    i_first, i_last = get_firt_index_value(first, last)
    email: str = dev[1]
    prefix = email.split("@")[0]
    return name, first, last, i_first, i_last, email, prefix

# normalize_text is now covered by preprocess_text

def bird_heuristic(pair1, pair2):
    name1, email1 = pair1["name"], pair1["email"]
    name2, email2 = pair2["name"], pair2["email"]

    # Pre-process both developers (reuse your process function)
    name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a = process((name1, email1))
    name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b = process((name2, email2))

    # Bird heuristic conditions
    c1 = calculate_similarity(name_a, name_b)
    c2 = calculate_similarity(prefix_b, prefix_a)
    c31 = calculate_similarity(first_a, first_b)
    c32 = calculate_similarity(last_a, last_b)
    c4 = c5 = c6 = c7 = False
    if i_first_a != "" and last_a != "":
        c4 = i_first_a in prefix_b and last_a in prefix_b
    if i_last_a != "":
        c5 = i_last_a in prefix_b and first_a in prefix_b
    if i_first_b != "" and last_b != "":
        c6 = i_first_b in prefix_a and last_b in prefix_a
    if i_last_b != "":
        c7 = i_last_b in prefix_a and first_b in prefix_a

    return {
        'name_1': name1,
        'email_1': email1,
        'name_2': name2,
        'email_2': email2,
        'c1': c1,
        'c2': c2,
        'c3.1': c31,
        'c3.2': c32,
        'c4': c4,
        'c5': c5,
        'c6': c6,
        'c7': c7
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
