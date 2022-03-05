#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python scripts that exports words from a spaCy dictionary to vectors, based on
the word2vec algorithm [Mikolov et al., 2015].
"""

from typing import Union

MAJOR: Union[int, str] = 0
MINOR: Union[int, str] = 1
PATCH: Union[int, str] = 0
DEV: Union[int, str, None] = None

__version__: str = f'{MAJOR}.{MINOR}.{PATCH}'
if DEV is not None:
	__version__ += f'.dev{DEV}'
