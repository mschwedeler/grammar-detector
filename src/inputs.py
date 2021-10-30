from spacy.tokens import Doc
from .nlp import nlp


class Input:
    """A helper class for tokenizing text and fragmenting the result into a `list[Doc]`. All properties must return a `list[Doc]` for compatibility purposes, hence the `docs` property."""

    def __init__(self, raw_input: str, extract_noun_chunks: bool = False) -> None:
        self.raw: str = raw_input
        self.doc: Doc = nlp(raw_input)
        self.extract_noun_chunks: bool = extract_noun_chunks

    @property
    def docs(self) -> list[Doc]:
        """Wrap the core Doc in a list for compatibility purposes."""
        return [self.doc]

    @property
    def noun_chunks(self) -> list[Doc]:
        """Get all of the nouns as Docs from the core Doc."""
        return [span.as_doc() for span in self.doc.noun_chunks]

    @property
    def fragments(self) -> list[Doc]:
        """Automatically select the most appropriate fragmenting attribute."""
        if self.extract_noun_chunks:
            return self.noun_chunks
        return self.docs
