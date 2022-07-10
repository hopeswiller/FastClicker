TESTS = tests/
START_MODULE = app.py
CODE_DIR = src


help: ##   		Output available commands
	@echo "Commands to control the project"
	@echo "Available commands:"
	@echo 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	@echo
	@echo "run-app			Start running application"
	@echo "run-tests		Run all test on the project"
	@echo "build-app		Compiles and builds app into an Executable"
	@echo "check-linting	Checks and formats code base"
	@echo "create-setup-env	Create virtual environment with required dependencies"
	@echo "remove-setup-env	Remove virtual environment"
	@echo "requirements-file	Generated a requirements file from pipfile"


run-app: 
	@echo "Starting application"
	@echo ".........................."
	@pipenv run python app.py

create-setup-env: 
	@echo "Setting up project..."
	@echo "Installing pipenv..."
	@pip install --upgrade pip
	@pip install pipenv
	@echo "Creating virtual environment and Installing requirements..."
	@pipenv install

remove-setup-env:
	@echo "Removing project virtualenv..."
	@pipenv --rm

requirements-file:
	@echo "Compiling Requirements File"
	@pipenv requirements > requirements.txt
	@echo "Done... "

run-tests:
	@pipenv run pytest -v --cache-clear --cov=${CODE_DIR} --cov-report=html ${TESTS}

build-app:
	@echo "Build Application into Executable"
	@rm -rf build/ 
	@rm -rf dist/
	@pipenv run python setup.py clean
	@pipenv run python setup.py bdist_msi 
	@rm -rf build/bdist.win*/
	@echo "Done..."

check-linting:
	@pipenv run black ${CODE_DIR}
	@pipenv run black ${START_MODULE}
	@pipenv run black ${TESTS}
	@pipenv run flake8 --verbose ${CODE_DIR}