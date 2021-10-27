from spacy.tokens import Doc
from settings import pattern_set_config_values
from .Match import Match, RawMatch


class MatchSet:
    def __init__(self, raw_matches: list[RawMatch], doc: Doc) -> None:
        self.matches = [Match(raw_match, doc) for raw_match in raw_matches]
        self.doc: Doc = doc
        self.best_match = pattern_set_config_values.prop_str("LONGEST_MATCH")

    @property
    def all(self):
        return self.matches

    @property
    def best(self):
        longest_match_setting = pattern_set_config_values.prop_str("LONGEST_MATCH")
        if self.best_match.upper() == longest_match_setting.upper():
            return self.match_longest(doc)

    @property
    def longest(self):
        logger.debug(f"Getting the longest match of these: {matches}")
        distances: list[int] = [match.end - match.start for match in self.matches]
        largest_distance_i: int = distances.index(max(distances))
        longest_match: Match = self.matches[largest_distance_i]
        logger.debug(f"Got the longest match: {longest_match}")
        return longest_match
