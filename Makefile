PYTHON   = python3


build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test

sdist:
	$(PYTHON) setup.py sdist

doc-html: build
	$(MAKE) -C doc html PYTHONPATH=$(CURDIR)

doc-pdf: build
	$(MAKE) -C doc latexpdf PYTHONPATH=$(CURDIR)

clean:
	rm -rf build
	rm -rf __pycache__

distclean: clean
	rm -f MANIFEST _meta.py
	rm -rf dist
	rm -rf tests/.pytest_cache
	$(MAKE) -C doc distclean

meta:
	$(PYTHON) setup.py meta


.PHONY: build test sdist doc-html doc-pdf clean distclean meta
