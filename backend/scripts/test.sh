#!/bin/bash
poetry run pytest --cov=app --cov-report=term-missing --cov-fail-under=50
