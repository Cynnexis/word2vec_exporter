#!/usr/bin/env python
# -*- coding: utf-8 -*-
from spacy.lexeme import Lexeme
import json
from typing import Dict, Union, List, Optional, Any

from word2vec_exporter.types import KeyTransform, JsonIndentation
from word2vec_exporter.exporter.abstract_exporter import AbstractExporter


class JsonExporter(AbstractExporter):

	def __init__(
		self,
		output: str,
		encoding: str = 'utf-8',
		indent: JsonIndentation = None,
		hash_key: bool = False,
		ignore_null: bool = True,
		lexeme_to_key_fn: Optional[KeyTransform] = None,
	):
		super().__init__(output)
		self.encoding: str = encoding
		self.indent: JsonIndentation = indent
		self.hash_key: bool = hash_key
		self.ignore_null: bool = ignore_null
		self.lexeme_to_key_fn: KeyTransform = lexeme_to_key_fn if lexeme_to_key_fn is not None else lambda x: x.text
		self.lexemes: Dict[Union[str, int], List[float]] = {}

	@property
	def name(self) -> str:
		return 'json'

	def export(self, lexeme: Lexeme) -> None:
		if not self.ignore_null or lexeme.has_vector:
			self.lexemes[hash(lexeme) if self.hash_key else self.lexeme_to_key_fn(lexeme)] = [
				float(x) for x in lexeme.vector.tolist()
			] if lexeme.has_vector else None

	def commit(self) -> None:
		with open(self.output, mode='w', encoding=self.encoding) as fd:
			json.dump(self.lexemes, fd, indent=self.indent)

	def members(self) -> tuple:
		return (*super().members(), self.encoding, self.indent, self.hash_key, self.lexemes)

	def __eq__(self, other) -> bool:
		return isinstance(other, JsonExporter) and self.members() == other.members()

	def __str__(self) -> str:
		return f'JsonExporter{{output: {self.output}, encoding: {self.encoding}, indent: {self.indent}, hash_key: {self.hash_key}, ignore_null: {self.ignore_null}, lexeme_to_key_fn: {self.lexeme_to_key_fn}}}'
	
	def __repr__(self) -> str:
		return f'JsonExporter{json.dumps(self.members())}'

	def __dict__(self) -> Dict[str, Union[str, JsonIndentation, bool, KeyTransform, Dict[Union[str, int], List[float]]]]:
		return {
			**super().__dict__(),
			'encoding': self.encoding,
			'indent': self.indent,
			'hash_key': self.hash_key,
			'ignore_null': self.ignore_null,
			'lexeme_to_key_fn': self.lexeme_to_key_fn,
			'lexemes': self.lexemes,
		}
