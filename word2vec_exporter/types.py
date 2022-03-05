from typing import Union, Callable
from spacy.lexeme import Lexeme

KeyTransform = Callable[[Lexeme], str]
JsonIndentation = Union[str, int, None]
