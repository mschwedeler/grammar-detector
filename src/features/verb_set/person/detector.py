from src.util.matcher import run_matcher
from src.util.transformer import make_doc
from .matcher import create_verb_person_matcher
from .validator import validate_person


def detect_verb_person(sentence_or_doc):
    doc = make_doc(sentence_or_doc)
    matcher = create_verb_person_matcher()
    match = run_matcher(matcher, doc)

    if not match:
        return ""
    (person, verb_span) = match
    validate_person(person)
    return person
