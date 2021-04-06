



def get_all_words(positive):
    for tokens in positive:
        for token in tokens:
            yield token


def get_tweets_for_model(token_list):
    for tweet_tokens in token_list:
        yield dict([token, True] for token in tweet_tokens)



