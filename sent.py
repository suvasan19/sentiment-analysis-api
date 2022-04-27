import nltk

import random
import pickle
from nltk.corpus import twitter_samples
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
from nltk import classify
from stop_words import get_stop_words

def clean_data(token):
    l = [item for item in token if not item.startswith("http") and not item.startswith("@")]
    remove = list(":'.*+,-/;=?^_&`~!")

    for item in l:
        item.str.replace(item,'',regex=True)

def remove_stop_words(token, stop_words):
    return [item for item in token if item not in stop_words]

def transform(token):
    result = {}
    for item in token:
        result[item] = True
    return result

def main():
    # Step 1: Gather data
    positive_tweets_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweets_tokens = twitter_samples.tokenized('negative_tweets.json')
    
    # Step 2: Clean, Lemmatize, and remove Stop Words
    stop_words = get_stop_words('en')
    positive_tweets_tokens_cleaned = [remove_stop_words(clean_data(token), stop_words) for token in positive_tweets_tokens]
    negative_tweets_tokens_cleaned = [remove_stop_words(clean_data(token), stop_words) for token in negative_tweets_tokens]
    
    # Step 3: Transform data
    positive_tweets_tokens_transformed = [(transform(token), "Positive") for token in positive_tweets_tokens_cleaned]
    negative_tweets_tokens_transformed = [(transform(token), "Negative") for token in negative_tweets_tokens_cleaned]

    # Step 4: Create data set
    dataset = positive_tweets_tokens_transformed + negative_tweets_tokens_transformed
    random.shuffle(dataset)
    train_data = dataset[:7000]
    test_data = dataset[7000:]
    # Step 5: Train data
    classifier = NaiveBayesClassifier.train(train_data)
    # Step 6: Test accuracy
    print("Accuracy is:", classify.accuracy(classifier, test_data))
    print(classifier.show_most_informative_features(10))
    # Step 7: Save the pickle
    f = open('my_classifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()

if __name__ == "__main__":
    main()