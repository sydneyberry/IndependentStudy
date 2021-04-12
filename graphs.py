import plotly.express as px
import pandas as pd
import calendar as cal
from datetime import datetime
from sklearn import metrics

positive_dates = []
negative_dates = []
neutral_dates = []

def init_this():
    for i in range(1, 11):  # should be 9 months
        positive_dates.append(0)
        negative_dates.append(0)
        neutral_dates.append(0)
    print(len(positive_dates), "  ", len(negative_dates), "  ", len(neutral_dates))



def add_date(label, date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # date = datetime.strptime(date_obj, "%a-%b-%d %H:%M:%S %z")
    if date_obj.month != 3:
        if label == "Positive":
            positive_dates[date_obj.month - 3] = positive_dates[date_obj.month - 3] + 1
        elif label == "Neutral":
            neutral_dates[date_obj.month - 3] = neutral_dates[date_obj.month - 3] + 1
        elif label == "Negative":
            negative_dates[date_obj.month - 3] = negative_dates[date_obj.month - 3] + 1


def just_checking():
    print("POS: ")
    for i in positive_dates:
        print("    ", i)
    print("NEG: ")
    for i in negative_dates:
        print("    ", i)
    print("NEU: ")
    for i in neutral_dates:
        print("    ", i)
    print(len(positive_dates))
    print(len(negative_dates))
    print(len(neutral_dates))


def calculate_percentages():
    pos_percent = []
    neg_percent = []
    neu_percent = []

    for i in range(len(positive_dates)):
        month_total = positive_dates[i] + negative_dates[i] + neutral_dates[i]
        if month_total > 0:
            pos_percent.append(positive_dates[i] / month_total * 100)
            neg_percent.append(negative_dates[i] / month_total * 100)
            neu_percent.append(neutral_dates[i] / month_total * 100)
        else:
            pos_percent.append(0)
            neg_percent.append(0)
            neu_percent.append(0)
    return pos_percent, neg_percent, neu_percent


def make_percentage_line_graph():
    pos_percent, neg_percent, neu_percent = calculate_percentages()
    print(len(pos_percent[1:]), "  ", len(neg_percent[1:]), "  ", len(neu_percent[1:]))
    print(len([cal.month_name[i] for i in range(4, 13)]))
    data = {'Months': [cal.month_name[i] for i in range(4, 13)],
            "Positive": pos_percent[1:],
            "Negative": neg_percent[1:],
            "Neutral": neu_percent[1:]}

    df = pd.DataFrame(data)
    fig = px.line(df,
                  x='Months',
                  y=['Positive', 'Neutral', 'Negative'],
                  title='Percentage of Tweets Classified Each Month',
                  labels={'variable': 'Sentiment',
                          'value': 'Percentage of Tweets'})
    fig.data[0].line.color = 'SeaGreen'  # positive
    fig.data[1].line.color = '#82c0d9'  # neutral
    fig.data[2].line.color = 'IndianRed'  # negative

    fig.write_html('percentage_graph.html', auto_open=True)


def make_total_line_graph():
    total_per_month = []
    for i in range(len(positive_dates)):
        total_per_month.append(positive_dates[i] + negative_dates[i] + neutral_dates[i])

    data = {'Months': [cal.month_name[i] for i in range(4, 13)],
            "Total": total_per_month[1:]}

    df = pd.DataFrame(data)
    fig = px.line(df,
                  x='Months',
                  y=['Total'],
                  title='Total Number of COVID-19 Related Tweets Per Month',
                  labels={'variable': 'Sentiment',
                          'value': 'Number of Geotagged Tweets in US related to COVID-19'})

    fig.data[0].line.color = 'DimGray'
    fig.write_html('total_graph.html', auto_open=True)


def make_pie_chart():
    total_pos = 0
    total_neg = 0
    total_neu = 0
    for i in range(len(positive_dates)):
        total_pos = total_pos + positive_dates[i]
        total_neg = total_neg + negative_dates[i]
        total_neu = total_neu + neutral_dates[i]

    x_data = [total_pos, total_neu, total_neg]
    names = ["Positive", "Neutral", "Negative"]
    fig = px.pie(values=x_data, names=names, title="Overall Sentiments of Tweets",
                 color=names,
                 color_discrete_map={'Positive': 'DarkSeaGreen',
                                     'Neutral': 'LightBlue',
                                     'Negative': 'IndianRed'})

    fig.write_html('pie_graph.html', auto_open=True)


#def confusion_matrix():

