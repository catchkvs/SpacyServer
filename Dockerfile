# Docker file for a slim Ubuntu-based Python3 image
FROM ubuntu:18.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

#ENV VIRTUAL_ENV=/opt/venv
#RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN mkdir app
RUN mkdir /app/models
COPY models /app/models/
COPY src/ /app/
COPY requirements.txt /app/requirements.txt
#RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz --no-deps
WORKDIR /app
RUN pip3 install -r requirements.txt
#RUN python3 -m spacy download en_core_web_sm
# Run the application:
EXPOSE 1050
#ENTRYPOINT [ "python" ]

CMD [ "python" , "-u", "app.py" ]