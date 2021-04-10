import csv

from nltk import FreqDist

import file_prep
import data_prep
import model
import pandas as pd
import random
from nltk import classify
from nltk import NaiveBayesClassifier

files_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy'
new_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\uncompiled_data'
compiled_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\compiled_data'
split_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\compiled_data\\split_labeled_data'


def call_stuff():
    negative_cleaned_tokens, positive_cleaned_tokens, neutral_cleaned_tokens, unlabeled_tweets = data_prep.make_json_file(
        split_data_location)
    all_positive_words = model.get_all_words(positive_cleaned_tokens)
    freq_dist_positive = FreqDist(all_positive_words)

    # Converting tokens to dictionary
    positive_tokens_for_model = model.get_tweets_for_model(positive_cleaned_tokens)
    negative_tokens_for_model = model.get_tweets_for_model(negative_cleaned_tokens)
    neutral_tokens_for_model = model.get_tweets_for_model(neutral_cleaned_tokens)

    # splitting the dataset for training and testing the model
    positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
    negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]
    neutral_dataset = [(tweet_dict, "Neutral") for tweet_dict in neutral_tokens_for_model]

    dataset = positive_dataset + negative_dataset + neutral_dataset
    random.shuffle(dataset)

    train_data = dataset[:548]
    test_data = dataset[548:]

    classifier = NaiveBayesClassifier.train(train_data)
    print("Accuracy is:", classify.accuracy(classifier, test_data))
    print(classifier.show_most_informative_features(10))

    # print(unlabeled_tweets)
    # for tweet in unlabeled_tweets:
    #    print(tweet)
    #    print(classifier.classify(dict([token, True] for token in tweet)))


#data_prep.count_labeled_data(compiled_data_location + "\\labeled_US_data.csv")
call_stuff()
