clean:
	rm -rf .coverage .eggs/ build/ deb_dist/ dist/ htmlcov/ python/cover python/nuc_wmi.egg-info nuc_wmi-*.tar.gz
	find . -type f -name "*~" -exec rm {} +
	find . -type f -name "*.pyc" -exec rm {} +
	find . -type d -name "__pycache__" -exec rmdir {} +

deb_py3: clean
	DEB_BUILD_OPTIONS=nocheck python3 setup.py --command-packages=stdeb.command bdist_deb

covtests: clean
	pylint python/nuc_wmi python/test/
	coverage run --branch --source python/nuc_wmi -m unittest discover --pattern "*_test.py" --start-directory python/ --verbose
	coverage report -m
	coverage html

test: clean
	pylint python/nuc_wmi python/test/
	python -m unittest discover --pattern "*_test.py" --start-directory python/ --verbose
