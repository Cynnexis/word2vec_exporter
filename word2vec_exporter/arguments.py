#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from typing import Optional, Sequence, List, Union
from typeguard import typechecked

from word2vec_exporter.types import KeyTransform, JsonIndentation
import word2vec_exporter as init_word2vec_exporter
from word2vec_exporter.exporter.abstract_exporter import AbstractExporter
from word2vec_exporter.exporter.json_exporter import JsonExporter


class AppArguments:
	"""
	Class to parse and store the parameters of this application.
	"""

	EXPORTER_VALUES: List[str] = ['json']
	DEFAULT_EXPORTER: str = EXPORTER_VALUES[0]

	KEY_TRANSFORM_VALUES: List[str] = ['text', 'hash', 'lower', 'upper']
	DEFAULT_KEY_TRANSFORM: str = KEY_TRANSFORM_VALUES[0]

	JSON_INDENT_STR_VALUES: List[str] = ['compact', 'tab', 'tabs', 'space', 'spaces']
	DEFAULT_JSON_INDENT: JsonIndentation = JSON_INDENT_STR_VALUES[0]

	DEFAULT_VERBOSE: bool = False

	DEFAULT_DEBUG: bool = False

	@typechecked
	def __init__(
		self,
		lang: str,
		output: Optional[str] = None,
		exporter: Union[str, AbstractExporter] = DEFAULT_EXPORTER,
		key_transform: Union[str, KeyTransform] = DEFAULT_KEY_TRANSFORM,
		json_indent: JsonIndentation = DEFAULT_JSON_INDENT,
		verbose: bool = DEFAULT_VERBOSE,
		debug: bool = DEFAULT_DEBUG,
	):
		self.lang = lang
		self.json_indent = json_indent
		self.verbose = verbose
		self.debug = debug

		# Parse "key_transform"
		self.key_transform: KeyTransform
		if isinstance(key_transform, str):
			if key_transform == 'text':
				self.key_transform = lambda lx: lx.text
			elif key_transform == 'hash':
				self.key_transform = lambda lx: lx.orth
			elif key_transform == 'lower':
				self.key_transform = lambda lx: lx.lower_
			elif key_transform == 'upper':
				self.key_transform = lambda lx: lx.text.upper()
			else:
				raise ValueError(
					f'Expected key_transform to be [{", ".join(self.KEY_TRANSFORM_VALUES)}], got "{key_transform}".')
		else:
			self.key_transform = key_transform

		# Parse "json_indent"
		self.json_indent: JsonIndentation
		if isinstance(json_indent, str):
			# Try convert it into a number
			try:
				self.json_indent = int(json_indent)

				if self.json_indent == 0:
					self.json_indent = None
			except ValueError:
				if self.json_indent == 'compact':
					self.json_indent = None
				elif self.json_indent == 'tab' or self.json_indent == 'tabs':
					self.json_indent = '\t'
				elif self.json_indent == 'space' or self.json_indent == 'spaces':
					self.json_indent = 2
				else:
					raise ValueError(
						f'Expected json_indent to be 0, a positive number or one of [{", ".join(self.JSON_INDENT_STR_VALUES)}], got "{json_indent}".'
					)

		# Parse "exporter"
		self.exporter: AbstractExporter
		if isinstance(exporter, str):
			if exporter == 'json':
				self.exporter = JsonExporter(
					output='output.json',
					indent=self.json_indent,
					lexeme_to_key_fn=self.key_transform,
				)
			else:
				raise ValueError(f'Expected exporter to be [{", ".join(self.EXPORTER_VALUES)}], got "{exporter}".')
		else:
			self.exporter = exporter

		# Parse "output"
		self.output: str
		if output is None:
			self.output = f'./{self.lang}.{self.exporter.name}'
		else:
			self.output = output

		self.exporter.output = self.output

	@classmethod
	def parse(cls, argv: Optional[Sequence[str]] = None):
		"""
		Constructor for `AppArguments`. It parse the given arguments.
		:param argv: The list of arguments to parse. If not given, it will
		default to `sys.argv`
		:return: Return the corresponding instance of `AppArguments`.
		"""
		p = argparse.ArgumentParser(
			prog='word2vec_exporter',
			description=init_word2vec_exporter.__doc__,
		)
		p.add_argument(
			'--lang',
			'-l',
			metavar='LANGUAGE',
			help=f"The language. It must be an installed spacy module name. Make sure that the module has vectors associated to its lexemes. See the full list here: https://github.com/explosion/spacy-models/blob/a82b4615a6ae547e99fe9514dc1137b344d8db4e/compatibility.json",
			required=True,
			type=str,
		)
		p.add_argument(
			'--output',
			'-o',
			metavar='FILE',
			help=f'The output file. If it exists, it will be overwritten. If none given, it defaults to the name of the given language, and the extension will depends of the exporter, in the current directory. For example, if you use the spaCy module "en_core_web_lg" with the JSON exporter, the output file will be "./en_core_web_lg.json".',
			default=None,
		)
		p.add_argument(
			'--exporter',
			'-e',
			metavar='EXPORTER',
			help=f'The name of the exporter. Defaults to "{cls.DEFAULT_EXPORTER}".',
			choices=cls.EXPORTER_VALUES,
			default=cls.DEFAULT_EXPORTER,
			type=str,
		)
		p.add_argument(
			'--key-transform',
			'-k',
			default=cls.DEFAULT_KEY_TRANSFORM,
			choices=cls.KEY_TRANSFORM_VALUES,
			help=f'The transformation to apply to the key. Defaults to "{cls.DEFAULT_KEY_TRANSFORM}".',
			type=str,
		)
		p.add_argument(
			'--json-indent',
			default=cls.DEFAULT_JSON_INDENT,
			help=f'The indentation. It can be a 0 (compact), a positive number or one of [{", ".join(cls.JSON_INDENT_STR_VALUES)}]. "space" and "spaces" will be replaced by 2 whitespaces. Defaults to "{cls.DEFAULT_JSON_INDENT}".',
			type=str,
		)
		p.add_argument(
			'--verbose',
			'-v',
			action='store_true',
			default=cls.DEFAULT_VERBOSE,
			help='Verbose mode.',
		)
		p.add_argument(
			'--debug',
			'-d',
			action='store_true',
			default=cls.DEFAULT_DEBUG,
			help='Debug mode.',
		)
		p.add_argument(
			'--version',
			'-V',
			action='version',
			version=f'%(prog)s 1.0.0',
			help='Print the version of the script and exit.')
		args = p.parse_args(argv)

		return AppArguments(
			lang=args.lang,
			output=args.output,
			exporter=args.exporter,
			key_transform=args.key_transform,
			json_indent=args.json_indent,
			verbose=args.verbose,
			debug=args.debug,
		)

	def members(self) -> tuple:
		return self.lang, self.verbose, self.debug

	def __eq__(self, other) -> bool:
		return isinstance(other, AppArguments) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())
