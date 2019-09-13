clean: clean-eggs clean-build clean-docs
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

clean-docs:
	@rm -fr docs/build/

pyformat:
	black . --exclude=docs

lint:
	flake8 . --exclude=docs

test:
	pytest -v --cov=pytest_stoq --cov-report=term-missing

checkall: pyformat lint test
