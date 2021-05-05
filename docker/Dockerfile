FROM ubuntu:18.04

ENV SPACY_VERSION=2.1.8
ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python-dev python3-pip python3-virtualenv git && \
    pip3 install --upgrade pip setuptools

RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

########################################
# spaCy
########################################
RUN pip3 install spacy==${SPACY_VERSION}
RUN python -m spacy download en_core_web_sm

COPY . /app
WORKDIR /app

# Install dependencies:
RUN pip3 install -r requirements.txt

# Run the application:
CMD ["python", "src/phrase_matching_rest.py"]