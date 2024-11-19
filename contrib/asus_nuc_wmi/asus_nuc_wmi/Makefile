clean:
	rm -rf .coverage .eggs/ build/ deb_dist/ dist/ htmlcov/ python/cover python/asus_nuc_wmi.egg-info asus_nuc_wmi-*.tar.gz
	find . -type f -name "*~" -exec rm {} +
	find . -type f -name "*.pyc" -exec rm {} +
	find . -type d -name "__pycache__" -exec rmdir {} +

deb_py3: clean
	DEB_BUILD_OPTIONS=nocheck python3 setup.py --command-packages=stdeb.command bdist_deb

covtests: clean
	pylint python/asus_nuc_wmi python/test/
	coverage run --branch --source python/asus_nuc_wmi -m unittest discover --pattern "*_test.py" --start-directory python/ --verbose
	coverage report -m
	coverage html

install_deb_build_deps:
	apt-get install -y debhelper dh-python fakeroot python-all python3-all python3-setuptools python3-wheel python3-stdeb

test: clean
	pylint python/asus_nuc_wmi python/test/
	python3 -m unittest discover --pattern "*_test.py" --start-directory python/ --verbose
