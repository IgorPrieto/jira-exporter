install:
	pip install -e .

test:
	pytest

run:
	jira-export --config config.json

summary:
	@ls relation_summary_*.csv

clean:
	rm -f *.csv
	find . -type f -name '__pycache__' -delete

.PHONY: install test run clean summary
