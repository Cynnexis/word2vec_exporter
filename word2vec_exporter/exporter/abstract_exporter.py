#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict
from spacy.lexeme import Lexeme
from abc import ABC, abstractmethod


class AbstractExporter(ABC):

	def __init__(self, output: str):
		self.output = output

	@property
	def name(self) -> str:
		raise NotImplementedError()

	@abstractmethod
	def export(self, lexeme: Lexeme) -> None:
		raise NotImplementedError()

	@abstractmethod
	def commit(self) -> None:
		raise NotImplementedError()

	def members(self) -> tuple:
		return self.lang, self.verbose, self.debug

	def __eq__(self, other) -> bool:
		return isinstance(other, AbstractExporter) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())

	def __str__(self) -> str:
		return f'AbstractExporter{{output: {self.output}}}'
	
	def __repr__(self) -> str:
		return f'AbstractExporter{json.dumps(self.members())}'

	def __dict__(self) -> Dict[str, str]:
		return {
			'output': self.output,
		}
