import pickle
import tweepy
from stop_words import get_stop_words
# from nltk.stem import WordNetLemmatizer
# from nltk.tag import pos_tag
# from textblob import TextBlob, Word

stop_words = get_stop_words('en')

def remove_stop_words(token, stop_words):
    return [item for item in token if item not in stop_words]

# def clean_data(token):
#     return [item for item in token if not item.startswith("http") and not item.startswith("@")]

def lemmatization(token):
    # lemmatizer = WordNetLemmatizer()
    # result = []
    # for token, tag in pos_tag(token):
    #     tag = tag[0].lower()
    #     print("tag ",tag[0])
    #     token = token.lower()
    #     print("token ",token)
    #     print("\n")
    #     if tag in "nva":
    #         result.append(lemmatizer.lemmatize(token, pos=tag))
    #     else:
    #         result.append(lemmatizer.lemmatize(token))
    # print("token",token)
    # result = TextBlob(token)
    
    # print(result)
    return token

def get_twitter_api():
    # personal details
    consumer_key = "Q7Su5Eu1urTKn9ZvMQ0hwtE6b"
    consumer_secret = "oMSaRZEkU3JnHxdtpS3O5FVM2HfUhbzeCExRZpVgDVZSVYsHEj"
    access_token = "1307733440637341697-Mi9URtcg9ka0otLBHLZ5iQY15q2Upq"
    access_token_secret = "tNepUuK5Gxr6B4wAWQi21oLCZrAUJi2mCYIApxVCEIoqj"
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

# This function uses the functions from the learner code above
def tokenize(tweet):
    return remove_stop_words(tweet, stop_words)

def get_classifier(pickle_name):
    f = open(pickle_name, 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier

def find_mood(search):
    classifier = get_classifier('my_classifier.pickle')
    api = get_twitter_api()
    stat = {
        "Positive": 0,
        "Negative": 0
    }
    pos = []
    neg = []
    for tweet in tweepy.Cursor(api.search_tweets, q=search, lang='en', count=100).items(100):
        custom_tokens = tokenize(tweet.text)
        category = classifier.classify(dict([token, True] for token in custom_tokens))
        stat[category] += 1
        if category == "Positive":
            pos.append(tweet.text)
        else:
            neg.append(tweet.text)

    print("The mood of", search)
    print(" - Positive", stat["Positive"], round(stat["Positive"]*100/(stat["Positive"] + stat["Negative"]), 1))
    print(" - Negative", stat["Negative"], round(stat["Negative"]*100/(stat["Positive"] + stat["Negative"]), 1))
    return {"count": [stat["Positive"], stat["Negative"]], "positive": pos, "negative" : neg }

if __name__ == "__main__":
    find_mood("arsenal")