export PYTHONPATH=.

help:
	@echo "clean        - remove artifacts"
	@echo "vendor       - install python requirements"
	@echo "loadmodel    - download nn models"
	@echo "vendorjs     - install npm packages"
	@echo "buildjs      - npm build"
	@echo "run          - flask run"
	@echo "test         - run python tests"
	@echo "build        - npm build + flask run"
	@echo "dockerbuild  - build docker image"
	@echo "dockerrun    - run service in docker"

.PHONY: vendor
vendor:
	pip install -r requirements.txt

.PHONY: loadmodel
loadmodel:
	@cd models; sh download.sh

.PHONY: vendorjs
vendorjs: clean
	@cd frontend; npm install

.PHONY: clean
clean:
	@find . -name '*.py[cod]' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*$py.class' -exec rm -rf {} +

.PHONY: buildjs
buildjs: clean
	@cd frontend; npm run build

.PHONY: run
run:
	PYTHONPATH=$(PYTHONPATH) python backend/service.py

.PHONY: test
test: clean
	PYTHONPATH=$(PYTHONPATH) python -m pytest ./tests -v

.PHONY: build
build: buildjs run

.PHONY: dockerbuild
dockerbuild:
	docker build -t valyaevilya/service-image-colorization:latest .

.PHONY: dockerrun
dockerrun:
	docker run -d -p 8080:8080 valyaevilya/service-image-colorization
