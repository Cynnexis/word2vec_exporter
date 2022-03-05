#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tqdm import tqdm
from spacy.lexeme import Lexeme
import spacy

import word2vec_exporter as init_word2vec_exporter
from word2vec_exporter.arguments import AppArguments
from word2vec_exporter.exporter.abstract_exporter import AbstractExporter
from word2vec_exporter.exporter.json_exporter import JsonExporter

__doc__ = init_word2vec_exporter.__doc__


def main(args: AppArguments):
	print(f'Loading module {args.lang}...')
	nlp = spacy.load(args.lang)
	lexeme: Lexeme
	for lexeme in tqdm(iterable=nlp.vocab, desc="Parsing lexemes", unit='lx'):
		args.exporter.export(lexeme)

	args.exporter.commit()


if __name__ == '__main__':
	main(AppArguments.parse())
