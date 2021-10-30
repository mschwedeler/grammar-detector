from spacy.tokens import Doc, Span
from .extractors import get_doc
from .nlp import nlp


class Input:
    """A helper class for tokenizing text and fragmenting the result into a list of Docs. This is required because of the support for extracting noun chunks, which is always a `list[Span]`. As such, a single `Doc` is wrapped in a `list`, hence the `docs` property."""

    def __init__(self, raw_input: str, extract_noun_chunks: bool = False) -> None:
        self.raw: str = raw_input
        self.doc: Doc = nlp(raw_input)
        self.extract_noun_chunks: bool = extract_noun_chunks

    @property
    def docs(self) -> list[Doc]:
        """Wrap the core Doc in a list for compatibility with the noun chunk extraction feature."""
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
