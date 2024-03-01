TRACKED_FILES=$(shell git ls-files '*.py')

format fmt:
	isort --profile black ${TRACKED_FILES}
	black ${TRACKED_FILES}

lint-only:
	pylint ${TRACKED_FILES}

lint: format lint-only

check-format:
	isort --profile black --check ${TRACKED_FILES}
	black --check ${TRACKED_FILES}
