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

subreddit_list = ['nuclearenergy', 'renewableenergy', 'france', 'environment', 'sustainability']
search_query = 'nuclear energy France'

posts = []

for subreddit_name in subreddit_list:
    subreddit = reddit.subreddit(subreddit_name)
    print(f"\nSubreddit: {subreddit_name}\n{'-'*30}")
    
    for submission in subreddit.search(search_query, limit=50): 
        if 'nuclear' in submission.title.lower():
            print(f"Title: {submission.title}")
            print(f"Score: {submission.score}")
            print(f"URL: {submission.url}")
            print(f"Posted on: {submission.created_utc}")
            print(f"Upvotes: {submission.ups}\n")

            post_date = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')

            submission.comments.replace_more(limit=0)  
            top_comments = sorted(submission.comments, key=lambda c: c.score, reverse=True)[:10]  

            comments_data = [comment.body for comment in top_comments] 

            posts.append({
                "post": submission.title,
                "comments": comments_data
            })

# Specify the CSV file name for nuclear energy posts
csv_file = 'nuclear_france_renewable_energy_reddit_posts_comments.csv'

# Write the nuclear energy-related scraped data to a CSV file in the desired format
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Post", "Comment"])  # Header row
    
    # Write each post with its associated comments
    for post in posts:
        for comment in post["comments"]:
            writer.writerow([post["post"], comment])

print(f"Data saved to {csv_file}")
