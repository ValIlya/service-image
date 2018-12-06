export PYTHONPATH=backend/venv/bin/python

help:
	@echo "clean        - remove artifacts"
	@echo "vendor       - install python requirements"
	@echo "vendorjs     - install npm packages"
	@echo "buildjs      - npm build"
	@echo "run          - flask run"
	@echo "build        - npm build + flask run"

vendor:
	pip install -r requirements.txt

vendorjs: clean
	@cd frontend; npm install

clean:
	@find . -name '*.py[cod]' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*$py.class' -exec rm -rf {} +

buildjs: clean
	@cd frontend; npm run build

run:
	PYTHONPATH=$(PYTHONPATH) python backend/app.py

build: buildjs run

