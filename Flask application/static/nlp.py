# Import libraries 
import nltk
import pickle

# The purpose of this script file is to load in the chossen NLP model ( Count vector ) and use it to predict the catergory based on the description entered for a job posting 

def nlpsuggestion(text_des,text_title):
    # Pre-process inputed text
    # Tokenise ----------------------------------------------------------------------
    text=text_des+text_title
    nl_text = text.lower() # cover all words to lowercase

    pattern = r'''(?x)          
    [a-zA-Z]+(?:[-'][a-zA-Z]+)?       #Regex expression extracts all words including those with - & ' embedded 
    '''
    tokenizer = nltk.RegexpTokenizer(pattern) 
    tokenised_text = tokenizer.tokenize(nl_text)
    # Remove 1 letter words ----------------------------------------------------------------------
    tokenised_text = [w for w in tokenised_text if len(w)>=2]
    # Remove stop words  ----------------------------------------------------------------------
    stopwords_ = []
    with open('./static/stopwords_en.txt') as f:
        stopwords_ = f.read().splitlines()
    # filter out stop words

    no_stops =[]
    for job in tokenised_text:
        if job not in stopwords_:
            no_stops.append(job)     

    tokenised_text = no_stops
    # Load model and vectorisor  ----------------------------------------------------------------------
    with open('./static/CountModel.pkl', 'rb') as f:
        CountVect, lr_model = pickle.load(f)

    count_features = CountVect.fit_transform([' '.join(tokenised_text)])

    return lr_model.predict(count_features)[0]
 