import praw
import pprint

# Could do this in one of two ways: look up the author of each submission to
# r/Iama and then go through each of the author's comments OR go through the
# comment of each submission and check if the comment author is the post author

r = praw.Reddit('AMA Summarizer by u/w4ngatang v 0.1.'
                'URL: forthcoming')

r.login()
covered = set()

# get new submissions
subreddit = r.get_subreddit('iama')
testing = r.get_subreddit('bottesting')
for submission in subreddit.get_hot(limit=1):

    # create empty dictionary
    msg = ""

    # get all the responses posted by AMA author
    author = r.get_redditor(submission.author)
    responses = author.get_comments(limit = 3)
    for response in responses:
         url = response.link_url + response.parent_id[3:]
         s = r.get_submission(url)
         question = s.comments[0]
         msg = msg + "\n\nQ: " + "[" + question.body + "](" + url + ")"  + "\n\nA: " + response.body
    r.submit(testing, title="AMASummary1", text=msg)
