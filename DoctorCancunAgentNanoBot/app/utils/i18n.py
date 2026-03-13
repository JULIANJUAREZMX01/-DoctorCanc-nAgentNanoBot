"""Language detection."""
EN = ["hello","hi ","hey ","good morning","how much","do you","can you","repair","fix","broken","screen","price","thanks"]
def detect_language(text):
    t = text.lower()
    return "en" if sum(1 for i in EN if i in t) >= 2 else "es"
