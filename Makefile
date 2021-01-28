.PHONY: build

build:
	rm dist/*
	python setup.py sdist bdist_wheel

add:
	pip install dist/midd-*.whl

remove:
	pip uninstall midd -y

publish-test:
	python3 -m twine upload -r testpypi dist/*

publish:
	python3 -m twine upload -r pypi dist/*
