FROM ufoym/deepo:caffe-py36-cpu

RUN apt-get update
RUN apt-get -y upgrade
# installing newer versions of node and npm
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN curl -L https://www.npmjs.com/install.sh | sh
RUN npm install -g npm@6 # version control

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PROJECT_ROOT=/app

COPY requirements.txt $PROJECT_ROOT/requirements.txt

RUN pip3 install -r $PROJECT_ROOT/requirements.txt --no-cache-dir

COPY . $PROJECT_ROOT

# build npm
WORKDIR $PROJECT_ROOT/frontend

 RUN npm install --no-optional
 RUN npm run build

WORKDIR $PROJECT_ROOT

CMD python3 backend/app.py