from logging import getLogger
from spacy import load as spacy_load
from spacy.language import Language
from settings import SPACY_DATASET


logger = getLogger(__name__)
logger.info(f"Started loading the spaCy model with the dataset '{SPACY_DATASET}'")

# Don't forget to run (with the appropriate dataset):
# $ python -m download en_core_web_lg
nlp: Language = spacy_load(SPACY_DATASET)
logger.info("Finished loading the spaCy model")
