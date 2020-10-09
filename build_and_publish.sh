rm -frv build
rm -frv dist
rm -frv *.egg-info
python setup.py sdist bdist_wheel
python -m twine upload --repository pypi dist/*
