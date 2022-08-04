from logging import getLogger
from typing import Union
from settings import pattern_set_config
from .Pattern import Pattern, PatternData


Name = str
MetaSetting = Union[str, bool]
Meta = dict[str, MetaSetting]

TestInput = str
TestExpectedRulenames = list[str]
TestExpectedSpans = list[str]
Test = dict[str, Union[TestInput, TestExpectedRulenames, TestExpectedSpans]]

PatternSetData = dict[str, Union[Meta, list[PatternData], list[Test]]]
ExtractedPatternSetData = tuple[Meta, list[PatternData], list[Test]]


logger = getLogger(__name__)


def extract_pattern_set_data(data: PatternSetData) -> ExtractedPatternSetData:
    """Extract and return the patterns, meta config, and tests from the loaded PatternSetData."""
    logger.info("Extracting the PatternSet data")

    logger.debug("Extracting the patterns")
    pattern_data_list: list[PatternData] = data["patterns"]

    logger.debug("Extracting the meta config")
    meta: Meta = data["meta"] if "meta" in data else {}

    logger.debug("Extracting the tests")
    tests: list[Test] = data["tests"] if "tests" in data else []

    return (pattern_data_list, meta, tests)


class PatternSet:
    def __init__(self, name: Name) -> None:
        logger.debug(f"Constructing the '{name}' PatternSet")
        self.name: Name = name
        self.patterns: dict[str, Pattern] = {}
        self.meta: Meta = {}
        self.tests: list[Test] = []

    @property
    def how_many_matches(self) -> str:
        try:
            return str(self.meta["how_many_matches"])
        except:
            return pattern_set_config.prop_str("ONE_MATCH")

    @property
    def should_extract_noun_chunks(self) -> bool:
        try:
            return bool(self.meta["extract_noun_chunks"])
        except:
            return False

    def add_pattern(self, pattern: Pattern) -> None:
        logger.info(
            f"Adding the '{pattern.rulename}' Pattern to the '{self.name}' PatternSet"
        )
        self.patterns[pattern.rulename] = pattern

    def get_all_patterns(self) -> list[Pattern]:
        logger.info(f"Getting all '{self.name}' PatternSet instances")
        return [self.patterns[k] for k in self.patterns]
