clean:
	rm -rf django_admin_cli.egg-info/ build/ coverage_html_report .coverage

test:
	python setup.py test

install:
	python setup.py install

build:
	python setup.py build

register:
	version=`python -c 'import admin_cli; print(admin_cli.__version__)'`
	git rev-parse ${version} &> /dev/null
	if [[ "$?" -eq 0 ]] ; then
	    echo "Version '${version}' already exists."
	    exit 1
	fi
	git tag -a ${version} -m "Version ${version}"
	git push origin ${version}
	python setup.py register
