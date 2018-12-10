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

vendor:
	pip install -r requirements.txt

loadmodel:
	@cd models; sh download.sh

vendorjs: clean
	@cd frontend; npm install

clean:
	@find . -name '*.py[cod]' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*$py.class' -exec rm -rf {} +

buildjs: clean
	@cd frontend; npm run build

run:
	PYTHONPATH=$(PYTHONPATH) python backend/service.py

test:
	PYTHONPATH=$(PYTHONPATH) python -m pytest ./tests -v

build: buildjs run

dockerbuild:
	docker build -t valyaevilya/service-image-colorization:latest .

dockerrun:
	docker run -d -p 8080:8080 valyaevilya/service-image-colorization
