import asyncio
import logging
from spacy.matcher import Matcher as SpacyMatcher
from . import validators
from .extractors import extract_span_features
from .nlp import nlp


logger = logging.getLogger(__name__)


class Matcher:
    def __init__(self, pattern_set):
        self.pattern_set = pattern_set

        logger.debug("Constructing the internal spaCy matcher")
        self._inner_matcher = SpacyMatcher(nlp.vocab, validate=True)

        logger.debug("Adding the patterns to the internal matcher")
        for pattern in self.pattern_set.get_all_patterns():
            rulename = pattern.rulename
            tokens = pattern.tokens
            config = {
                "greedy": "LONGEST",
                "on_match": self._on_match,
            }
            logger.debug(f"Adding the pattern '{rulename}' to the internal matcher")
            self._inner_matcher.add(rulename, [tokens], **config)

    def match(self, doc):
        """The entry point for running the matcher. Using the pattern set provided
        during construction, the appropriate matcher method will be returned.
        All usable matcher methods should be included here."""
        how_many_matches = self.pattern_set.how_many_matches
        logger.debug(f"Running the matcher method for '{how_many_matches}' result(s)")
        if how_many_matches == "ONE":  # Refactor
            return self._match_one(doc)
        elif how_many_matches == "MANY":  # Refactor
            return self._match_all(doc)
        else:
            return self._match_one(doc)

    def _match_one(self, doc):
        logger.debug("Matching for one result")
        logger.debug("Running the internal matcher")
        all_matches = self._inner_matcher(doc)
        logger.debug(f"Found {len(all_matches)} match(es)")

        logger.debug("Determining the best match")
        best_match = self._get_best_match(all_matches)

        logger.debug(f"Parsing the best match: {best_match}")
        parsed_match = self._parse_match(best_match, doc)

        logger.debug(f"Parsed the best match: {parsed_match}")
        return parsed_match

    def _match_all(self, doc):
        logger.debug("Matching for all results")
        logger.debug("Running the internal matcher")
        all_matches = self._inner_matcher(doc)
        logger.debug(f"Found {len(all_matches)} match(es)")

        logger.debug(f"Parsing many matches: {all_matches}")
        parsed_matches = [self._parse_match(m, doc) for m in all_matches]

        logger.debug(f"Parsed many matches: {parsed_matches}")
        return parsed_matches

    def _on_match(self, matcher, doc, i, matches):
        logger.debug(f"MATCH #{i}")
        logger.debug("Running the on_match callback")
        logger.debug(f"External matcher: {self}")
        logger.debug(f"Internal matcher: {matcher}")
        logger.debug(f"Doc: {doc}")
        logger.debug(f"Matches: {matches}")

    def _parse_match(self, match, doc):
        (match_id, start, end) = match
        rulename = nlp.vocab.strings[match_id]
        span = doc[start:end]
        logger.debug(f"Parsed ('{rulename}', '{span}') from match '{match}'")
        return (rulename, span, extract_span_features(span))

    def _get_best_match(self, matches):
        # TODO get longest match
        try:
            return matches[-1]
        except IndexError:
            msg = f"No matches were found"
            logger.error(msg)
            raise Exception(msg)
