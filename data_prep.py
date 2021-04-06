import os
import csv as csv

from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re, string
from nltk.corpus import stopwords

from nltk.tag import (pos_tag)

import jsonlines
from datetime import datetime
from nltk.tokenize import word_tokenize

import io

stoplist = set(stopwords.words('english'))
files_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy'
neg_data_list = []
pos_data_list = []
unlabeled_data_list = []

positive_cleaned_tokens = []
negative_cleaned_tokens = []
unlabeled_cleaned_tokens = []


def extract_data(location):
    output_file = location + "\\unlabeled_US_data.csv"
    input_file = location + "\\hydrated_compiled_data.jsonl"
    if not os.path.exists(input_file):
        print("uh oh better fix that")
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'w+', newline='', encoding="utf8") as writefile:
        with jsonlines.open(input_file) as readfile:
            w = csv.writer(writefile)
            r = jsonlines.Reader(input_file)
            for row in readfile:
                obj = []
                if row['place'] is not None and row['place']['country_code'] == 'US':
                    orig_timedate = row['created_at']
                    date_obj = datetime.strptime(orig_timedate, "%a %b %d %H:%M:%S %z %Y")

                    obj.append(date_obj)
                    obj.append(row['id'])
                    obj.append(row['place']['country_code'])
                    obj.append(row['full_text'])
                    w.writerow(obj)


def count_labeled_data(location):
    neutral = 0
    positive = 0
    negative = 0

    with open(location, 'r', newline='', encoding='utf8') as readfile:
        r = csv.reader(readfile, delimiter=',')
        for row in r:
            if row[4] == "1":
                positive = positive + 1
            elif row[4] == "0":
                neutral = neutral + 1
            elif row[4] == "-1":
                negative = negative + 1
    print("Positive: " + str(positive))
    print("Neutral: " + str(neutral))
    print("Negative: " + str(negative))


def make_json_file(folder_location):
    csv_file = folder_location + "\\all_labeled_data.csv"
    pos_file = folder_location + "\\positive_data.json"
    neg_file = folder_location + "\\negative_data.json"
    unlabeled_file = folder_location + "\\unlabeled_data.json"

    total = 0
    with open(pos_file, 'w+', newline='', encoding="utf8") as pos_data, \
            open(neg_file, 'w+', newline='', encoding="utf8") as neg_data, \
            open(unlabeled_file, 'w+', newline='', encoding="utf8") as unlabeled_data:

        with open(csv_file, 'r', newline='', encoding='utf-8') as readfile:
            fieldnames = ("date", "tweet_id", "country_code", "text", "label")
            reader = csv.DictReader(readfile, fieldnames)
            for row in reader:
                # call to clean data here
                if row['label'] == "-1":
                    initial_clean_tweet = clean_tweet(row['text'])
                    if initial_clean_tweet != "":
                        #neg_data_list.append(word_tokenize(initial_clean_tweet))
                        negative_cleaned_tokens.append(lemm_data(word_tokenize(initial_clean_tweet), stoplist))
                        # json.dump(row, neg_data)  # do I even need ???
                elif row['label'] == "1":
                    initial_clean_tweet = clean_tweet(row['text'])
                    if initial_clean_tweet != "":
                        #pos_data_list.append(word_tokenize(initial_clean_tweet))
                        positive_cleaned_tokens.append(lemm_data(word_tokenize(initial_clean_tweet), stoplist))
                        # json.dump(row, pos_data)
                else:
                    initial_clean_tweet = clean_tweet(row['text'])
                    if initial_clean_tweet != "" and initial_clean_tweet != " ":
                        #unlabeled_data_list.append(word_tokenize(initial_clean_tweet))
                        unlabeled_cleaned_tokens.append(lemm_data(word_tokenize(initial_clean_tweet), stoplist))

                        # json.dump(row, unlabeled_data)

    # normalize/lemmatize tokens
    #for tweet in neg_data_list:
     #   negative_cleaned_tokens.append(lemm_data(tweet, stoplist))
    #for tweet in pos_data_list:
    #   positive_cleaned_tokens.append(lemm_data(tweet, stoplist))
    #for tweet in unlabeled_data_list:
     #   unlabeled_cleaned_tokens.append(lemm_data(tweet, stoplist))

    return negative_cleaned_tokens, positive_cleaned_tokens, unlabeled_cleaned_tokens


def clean_tweet(data):
    location = 0
    while True:
        location = data.find('@', location + 1)
        location = int(location)
        if location == -1:
            break
        elif location < len(data):
            if data[location + 1] == ' ':
                data = data[: location]
                break
            else:
                space_location = data.find(' ')
                data = data[location: space_location]

    # Remove URL's
    data = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', data)
    # Remove numbers
    data = re.sub(r'[0-9]', '', data)
    # Remove unknown symbols (like emojis)
    data = re.sub(r'[^\x00-\x7f]', '', data)
    # Remove Emails
    data = re.sub(r'\S*@\S*\s?', '', data)
    # Remove new line characters
    data = re.sub(r'\s+', ' ', data)

    return data.lower()


def lemm_data(tweet_tokens, stop_words=()):
    print("lemm data", tweet_tokens)
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        if token == "'s":
            token = "is"
        elif token == "'ve":
            token = "have"
        elif token == "covid-" or token == "corona" or token == "coronavirus":
            token = "covid"

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(positive):
    for tokens in positive:
        for token in tokens:
            yield token

def get_tweets_for_model(token_list):
    for tweet_tokens in token_list:
        yield dict([token, True] for token in tweet_tokens)


# OLD: built for using a jsonl file converted to csv
def extract_needed_data():
    all_hydrated_data = files_location + "/hydrated_data.csv"
    output_file = files_location + "/US_data_UNLABELED.csv"
    if not os.path.exists(all_hydrated_data):
        print("not cool")
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'w+', newline='', encoding="utf8") as writefile:
        with open(all_hydrated_data, encoding="utf8") as readfile:
            r = csv.reader(readfile, delimiter=',')
            w = csv.writer(writefile)
            for row in r:
                row_data = []
                colCount = 0
                for cell in range(len(row)):
                    cell_data = row[cell]
                    if cell_data[:14] == '{"created_at":':
                        date_string = cell_data[15:(len(cell_data) - 1)]
                        # reformat timestamp
                        date_obj = datetime.strptime(date_string, "%a %b %d %H:%M:%S %z %Y")
                    if cell_data[:3] == "id:" and len(row_data) == 1:
                        tweet_id = cell_data[3:(len(cell_data) - 1)]
                    if colCount == 3:
                        full_text = cell_data[11:]
                    if (colCount == 4 or colCount == 5 or colCount == 6) and (
                            cell_data != "truncated:false" and cell_data[:19] != "display_text_range:"):
                        full_text = full_text + " " + cell_data
                    # if cell_data[:10] == "full_text:":
                    # full_text = cell_data[11:]
                    if cell_data[:13] == "country_code:":
                        country_code = cell_data[14:(len(cell_data) - 1)]
                    colCount = colCount + 1

                if country_code == "US":
                    row_data.append(date_obj)
                    row_data.append(country_code)
                    row_data.append(full_text)
                    if len(row_data) == 3:
                        w.writerow(row_data)
    print("Done extracting.")
