#!/usr/bin/env bash

isort .
black .
autoflake . --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude=__init__.py
