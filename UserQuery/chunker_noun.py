from nltk.tag import pos_tag
    
# Main method, just run "python np_extractor.py"
def extract(query):
    sentence = query
    tagged_sent = pos_tag(sentence.split())
    propernouns = [word for word,pos in tagged_sent if pos == 'NN']   
    return propernouns

#extract("I want to buy a car and a dog and plane")