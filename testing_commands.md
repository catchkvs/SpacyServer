### Testing using curl commands

Programming Model testing using curl

`
curl -d '{"text":"I have 12 years of experience in java and j2ee technologies in a agile environment"}' -H "Content-Type: application/json" -X POST http://localhost:1050/extract-ner
{
  "java": "Programming Language"
}


#### Extract NLP Attributes of a sentence
`curl -d '{"text":"What dishes you have in Rice"}' -H "Content-Type: application/json" -X POST http://localhost:1050/nlp/attributes`

#### Extract relations
`curl -d '{"text":"Net income was $9.4 million compared to the prior year of $2.7 million."}' -H "Content-Type: application/json" -X POST http://localhost:8050/extract-relation`

`curl -d '{"text":"I have 12 years of experience in java and j2ee technologies in a agile environment"}' -H "Content-Type: application/json" -X POST http://spacy.interviewparrot.com/extract-ner`