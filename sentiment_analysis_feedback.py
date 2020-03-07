import pandas as pd
import numpy as np
from textblob import TextBlob

class Feedback:
    def __init__(self):
        self.data1 = pd.read_csv('1429_1.csv')
        self.data2 = pd.read_csv('Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv')
        self.data3 = pd.read_csv('Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv')
        
    def clean_data(self):
        reviews = np.array(self.data1['reviews.text'])
        reviews = np.append(reviews, self.data2['reviews.text'])
        reviews = np.append(reviews, self.data3['reviews.text'])
        return reviews
        
    def get_review_sentiment(self,review):
        analysis = TextBlob(review)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
    def get_data(self):
        analysis = []
        reviews = self.clean_data()
        for review in reviews:
            parsed_review = {}
            parsed_review['text'] = review
            parsed_review['sentiment'] = self.get_review_sentiment(str(review))
            analysis.append(parsed_review)
        return analysis
    
def main():
    ob = Feedback()
    reviews = ob.get_data()
    previews = [review for review in reviews if review['sentiment'] == 'positive']
    nreviews = [review for review in reviews if review['sentiment'] == 'negative']
    print('Positive reviews percentage: {} %'.format(100*len(previews)/len(reviews)))
    print('Negative reviews percentage: {} %'.format(100*len(nreviews)/len(reviews)))
    print('Neutral reviews percentage: {} %'.format(100*(len(reviews) - len(previews) - len(nreviews))/len(reviews)))
    
if __name__ == "__main__" :
    main()