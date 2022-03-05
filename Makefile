#!/usr/bin/env make
SHELL := /bin/bash
.ONESHELL:

.PHONY: help
help:
	@echo 'Makefile for word2vec_exporter'
	echo
	echo 'usage: make [command]'
	echo
	echo 'Command:'
	echo "  configure         - Configure the project folder."
	echo "  configure-git     - Configure the project folder for git usage. Use 'configure' for global configuration of the project."
	echo

.git/hooks/pre-commit:
	curl -fsSL "https://gist.githubusercontent.com/Cynnexis/cd7fdc7b911ac39b623a3a62105e7d45/raw/pre-commit" -o ".git/hooks/pre-commit"
	@if command -v "dos2unix" > /dev/null 2>&1; then \
		dos2unix ".git/hooks/pre-commit"; \
	else \
		echo "dos2unix not found. If you are on Windows, you may consider installing it."; \
	fi

.PHONY: configure-git
configure-git: .git/hooks/pre-commit

.PHONY: configure
configure: configure-git
