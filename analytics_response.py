from analytics.helper_funcs import read_weekly_data
from model_apis.chatgpt import send_to_chatgpt
import matplotlib.pyplot as plt


class Analytics():
    def __init__(self):
        self.weekly_data = read_weekly_data()
        
    def weekly_exercise_analytics(self):
        prompt = """Please give a brief overview of the exercise activities from the past week and the biggest exercise accomplishment.
                Format it as such: A sentence or two on a summary, a section with more details for each type of activity, and a sentence or two on the 
                biggest exercise accomplishment. You can finish with a word of encouragement or challenge for the week ahead. \n Data: \n""" + self.weekly_data
        response = send_to_chatgpt(prompt)
        return response

    def weekly_social_analytics(self):
        prompt = """Please give a brief overview of the social activities from the past week. Format it as such: 
                A sentence or two on a summary, a section with more details for each type of activity, and a sentence or two on the 
                highlight. You can finish with a word of encouragement or challenge for the week ahead. \n Data: \n""" + self.weekly_data
        response = send_to_chatgpt(prompt)
        return response
    
    def weekly_music_analytics(self):
        prompt = """Please respond with music trends over the past week. The output will be structured as such:
                    Genre distribution: <breakdown of distribution>. \n Top 3 songs of the week: <list of top songs with artists>. \n Data: \n""" + self.weekly_data
        response = send_to_chatgpt(prompt)
        return response
    
    def get_sent_scores(self):
        prompt = """Please give a sentiment score for each overall diary entry. They are seperated by the words 'diary entry' in the data text.
                    You should respond only with seven numeric values, one for each of the past 7 days. These scores will range from [0-10]. 
                    Make the values represent a good range overall, ranging according to the other days to see the relative sentiments. 
                    Make the values comma seperated with no spaces. \n Data: \n""" + self.weekly_data
        response = send_to_chatgpt(prompt)
        values = [float(i) for i in response.split(",")]
        return values
    
    def plot_sent_scores(self):
        sent_scores = self.get_sent_scores()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        plt.figure(figsize=(10, 5))
        plt.plot(days, sent_scores, marker='o',linestyle='--', color='teal', linewidth=2) 

        plt.ylim(0, 10)
        plt.title("Weekly Sentiment Scores")
        plt.xlabel("Day")
        plt.ylabel("Sentiment Score")
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.axhline(0, color='grey', linewidth=0.5)
        
        for i, score in enumerate(sent_scores):
            plt.annotate(f"{score:.2f}", (days[i], sent_scores[i]), textcoords="offset points", xytext=(0,10), ha='center')

        plt.yticks(fontsize=12)
        plt.xticks(days, rotation=45, fontsize=12)
        plt.tight_layout()
        plt.legend(['Sentiment Score'], loc='lower right')

        plt.show()



test = Analytics()
print(test.plot_sent_scores())