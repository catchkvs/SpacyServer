import spacy
#nlp = spacy.load("en_trf_bertbaseuncased_lg")

def inferenceNER(model_dir, text) :
     # test the saved model
    print("Loading from", model_dir)
    nlp2 = spacy.load(model_dir)
    # Check the classes have loaded back consistently
    doc2 = nlp2(text)
    output_dict = {}
    for ent in doc2.ents:
        print(ent.label_, ent.text)
        output_dict[ent.label_] = ent.text
    return output_dict

#def similarity(sentence1, sentence2) :
#    doc1 = nlp(sentence1)
#    doc2 = nlp(sentence2)
#    return doc1[0].similarity(doc2[0])

def main():
    inferenceNER("/home/interviewparrot/ws/SpacyServer/models/programming_language", "I have been working in java j2ee technologies for 12 years")

if __name__ == "__main__":
    main()
