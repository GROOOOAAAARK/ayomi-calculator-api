.PHONY: install-project run

install-project:
	pipenv shell
	pipenv install --dev
	clear

run:
	python -m app start

