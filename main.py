import csv

from nltk import FreqDist

import file_prep
import data_prep
import model
import pandas as pd
import random
from nltk import classify
from nltk import NaiveBayesClassifier
import pickle
import graphs

files_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy'
new_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\uncompiled_data'
compiled_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\compiled_data'
split_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\compiled_data\\split_labeled_data'
accuracy = ""


def call_classifier():
    negative_cleaned_tokens, positive_cleaned_tokens, neutral_cleaned_tokens, unlabeled_tweets = data_prep.make_json_file(
        split_data_location)
    all_positive_words = model.get_all_words(positive_cleaned_tokens)
    # freq_dist_positive = FreqDist(all_positive_words)

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
    accuracy = classify.accuracy(classifier, test_data)
    save_classifier(classifier)

    print("ACCURACY: ", accuracy * 100, "%")
    print(classifier.show_most_informative_features(15))

    # print(unlabeled_tweets)
    # for tweet in unlabeled_tweets:
    #    print(tweet)
    #    print(classifier.classify(dict([token, True] for token in tweet)))


def label_unlabeled_data(classifier):
    graphs.init_this()
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    # clean data, label, and then graph accordingly
    with open(compiled_data_location + "\\machine_labeled.csv", 'w+', newline='',
              encoding="utf8") as unlabeled_write_file:
        with open(compiled_data_location + "\\labeled_US_data.csv", 'r', newline='', encoding='utf-8') as readfile:
            w = csv.writer(unlabeled_write_file)
            fieldnames = ("date", "tweet_id", "country_code", "text", "label")
            reader = csv.DictReader(readfile, fieldnames)
            for row in reader:
                # if positive_count >= 500 and negative_count >= 500:
                #    break

                if row['label'] == "":
                    initial_clean_tweet = data_prep.clean_tweet(row['text'])
                    if not initial_clean_tweet.isspace():
                        tokens = data_prep.lemm_data(data_prep.word_tokenize(initial_clean_tweet), data_prep.stoplist)
                        label = classifier.classify(dict([token, True] for token in tokens))
                        if label == "Positive":
                            positive_count = positive_count + 1
                            graphs.add_date(label, row['date'][:10])
                        elif label == "Negative":
                            negative_count = negative_count + 1
                            graphs.add_date(label, row['date'][:10])
                        elif label == "Neutral":
                            neutral_count = neutral_count + 1
                            graphs.add_date(label, row['date'][:10])
                        # print(classifier.classify(dict([token, True] for token in row)) + ":      " + row['text'])
                elif row['label'] == "1":
                    graphs.add_date(1, row['date'][:10])
                elif row['label'] == "0":
                    graphs.add_date(0, row['date'][:10])
                elif row['label'] == "-1":
                    graphs.add_date(-1, row['date'][:10])

    print("Positive: ", positive_count)
    print("Negative: ", negative_count)
    print("Neutral: ", neutral_count)

    graphs.make_percentage_line_graph()
    graphs.make_total_line_graph()
    graphs.make_pie_chart()


def save_classifier(classifer):
    with open('classifer.pickle', 'wb') as f:
        pickle.dump(classifer, f)


def load_classifer():
    f = open('classifer.pickle', 'rb')
    classifer = pickle.load(f)
    f.close()
    return classifer


if __name__ == "__main__":
    # call_classifier()
    classifier = load_classifer()
    label_unlabeled_data(classifier)
    print(classifier.show_most_informative_features(15))
