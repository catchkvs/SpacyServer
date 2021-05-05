# SpacyServer
The Natural language processing engine behind interviewparrot

### Prerequisites
   * pip 19.2.3
   * python 3.6.9
   * virtualenv 15.1.0

### Installation and usage   
   * Clone repository and cd to the root dir
   * `virtualenv  --python=python3.6 venv`
   * `source venv/bin/activate`
   * `pip install flask`
   * `flask --version`  should output 
      ```   
            Python 3.6.9
            Flask 1.1.1
            Werkzeug 0.16.0
       ```
    * Install spacy `pip install -U spacy`
    * Link model `python -m spacy download en_core_web_sm`

### Running server
   * `source  venv/bin/activate` 
   * python src/app.py
   * Server should now have started (default http://127.0.0.1:1050/)
   * Send curl post 
    ```
    curl -d '{"text":"I have 12 years of experience in java and j2ee technologies in a agile environment"}' -H "Content-Type: application/json" -X POST http://localhost:1050/extract-ner
    ```

### Running using docker
1. `docker build -t spacy-server:1.0 .`
2. `docker run -p 1050:1050 spacy-server:1.0`


* This will stop any existing container and rebuild image
   `docker-compose build`
* To just start and stop containers use
   `docker-compose up `, `docker-compose down`
   Or in detached (bg) mode `docker-compose up -d`
   
