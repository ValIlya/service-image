FROM ufoym/deepo:caffe-py36-cpu

# installing newer versions of node and npm
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get install -y nodejs && \
    curl -L https://www.npmjs.com/install.sh | sh && \
    npm install -g npm@6 # version control && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \

ENV PROJECT_ROOT=/app
COPY requirements.txt $PROJECT_ROOT/requirements.txt
RUN pip3 install -r $PROJECT_ROOT/requirements.txt --no-cache-dir
COPY . $PROJECT_ROOT

# building frontend
WORKDIR $PROJECT_ROOT/frontend
RUN npm install --no-optional
RUN npm run build

# Running app
WORKDIR $PROJECT_ROOT/
CMD make run