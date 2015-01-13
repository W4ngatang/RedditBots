import praw
import pprint
import time

MAX_LEN = 10000
RESPONSE_LIMIT = 10

r = praw.Reddit('AMA Summarizer by u/w4ngatang v 0.1.'
                'URL: https://github.com/W4ngatang/RedditBots')

r.login('AMASummaryBot', '9kSYpVcGV5h1HC31mpfj')
covered = set()

# get new submissions
subreddit = r.get_subreddit('iama')
testing = r.get_submission(submission_id='2rtg51')
for submission in subreddit.get_hot(limit=5):

    # check if AMA has finished
    # roughly determined if AMA is older than six hours
    current_time = int(time.time())
    author = r.get_redditor(submission.author)
    most_recent = author.get_comments(limit = 1)
    for recent in most_recent:
        elapsed = (current_time - recent.created_utc) / 60 / 60 
    if elapsed < 2:
        continue 

    # create empty dictionary
    msg = ""
    root = None

    # get all the responses posted by AMA author
    responses = author.get_comments(limit = RESPONSE_LIMIT)
    for response in responses:
        if response.submission == submission:
            url = response.link_url + response.parent_id[3:]
            s = r.get_submission(url)
            questions = s.comments[0]
            formatted = response.body.replace('\n', '\n>')
            tmp = msg + "\n\n[Q](" + url + "):" + questions.body + "\n\n> " + formatted
            if len(tmp) > MAX_LEN:
                if root == None:
                    root = testing.add_comment(msg)
                else:
                    root.reply(msg)
                msg = "" 
            msg = msg + "\n\n[Q](" + url + "):" + questions.body + "\n\n> " + formatted
    if root == None:
        root = testing.add_comment(msg)
    else:
        root.reply(msg)
    print(msg)
#    testing.add_comment(msg)
#    r.submit(testing, title="AMASummary2", text=msg)
