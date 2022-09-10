build:
	python setup.py bdist_wheel
clean:
	rm -r build dist *.egg-info .env
env:
	python -m venv .env
install-requirements:
	pip install -r requirements.txt
