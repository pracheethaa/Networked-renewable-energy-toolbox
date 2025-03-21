import praw
import sys
import csv
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

reddit = praw.Reddit(
    client_id="rMBDrCGgPLe50bULZeiArw",
    client_secret="RBxw86ppkdhNMYOJoAqdz8Us0sGkUw",
    user_agent="app-a",
    username="Pretend_North_2966"
)

subreddit_list = ['windenergy', 'renewableenergy', 'france', 'environment', 'sustainability']
search_query = 'wind energy France'

# Store posts data in a list of dictionaries
posts = []

for subreddit_name in subreddit_list:
    subreddit = reddit.subreddit(subreddit_name)
    print(f"\nSubreddit: {subreddit_name}\n{'-'*30}")
    
    for submission in subreddit.search(search_query, limit=100): 
        if 'wind' in submission.title.lower() and 'france' in submission.title.lower():
            print(f"Title: {submission.title}")
            print(f"Score: {submission.score}")
            print(f"URL: {submission.url}")
            print(f"Posted on: {submission.created_utc}")
            print(f"Upvotes: {submission.ups}\n")

            # Convert the created_utc timestamp to a readable format
            post_date = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')

            submission.comments.replace_more(limit=0)  
            top_comments = sorted(submission.comments, key=lambda c: c.score, reverse=True)[:10]  # Get top 10 most upvoted comnt

            comments_data = [comment.body for comment in top_comments] 

            posts.append({
                "post": submission.title,
                "comments": comments_data
            })

csv_file = 'wind_energy_france_comments.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Post", "Comment"]) 
    
    for post in posts:
        for comment in post["comments"]:
            writer.writerow([post["post"], comment])

print(f"Data saved to {csv_file}")
