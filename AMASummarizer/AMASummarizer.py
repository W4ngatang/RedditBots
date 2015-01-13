import praw
import pprint
import time

MAX_LEN = 10000                                         # max message length, set by reddit
RESPONSE_LIMIT = 10                                     # number of comments to pull at a time
SUB_LIMIT = 10                                          # number of submissions to pull at a time
SLEEP_TIME = 120                                        # amount of time to sleep
MSG_BASE = "Question | Answer \n ----------|----------" # base for summarizing

r = praw.Reddit('AMA Summarizer by u/w4ngatang v 0.1.'
                'URL: https://github.com/W4ngatang/RedditBots')

r.login('AMASummaryBot', '9kSYpVcGV5h1HC31mpfj')
summarized = [] 
summarizing = []

# go through summarizing list and update, removing into summarized if detect AMA finished
def summarize():
    for submission in summarizing:
        # create initial message, set up table
        msg = MSG_BASE 
        
        # base comment
        # if first message exceeds character limit, further posts will be replies to root
        root = None

        # get all the responses posted by AMA author
        author = r.get_redditor(submission.author)
        responses = author.get_comments(limit = RESPONSE_LIMIT)
        for response in responses:

            # if the response is for the AMA
            if response.submission == submission:

                # get the comment and its parent
                url = response.link_url + response.parent_id[3:]
                s = r.get_submission(url)
                question = s.comments[0]

                # formatting to make it fit in a table
                format_answer = response.body.replace('\n', ' ')
                format_question = question.body.replace('\n', ' ')

                # string to be added
                tmp = "\n[Q](" + url + "):" + format_question + " | " + format_answer

                # if the proposed msg would be too long, post the existing msg
                # and reset msg
                if len(msg + tmp) > MAX_LEN:
                    testing.add_comment(msg) if root == None else root.reply(msg)
                    # reset the msg
                    msg = MSG_BASE 

                # increment the message
                msg = msg + tmp 

        # post the message
        if len(msg) > len(MSG_BASE): 
            testing.add_comment(msg) if root == None else root.reply(msg)

        # check if AMA has finished
        # roughly determined if AMA is older than six hours
        current_time = int(time.time())
        most_recent = author.get_comments(limit = 1)
        for recent in most_recent:
            elapsed = (current_time - recent.created_utc) / 60 / 60 
        if elapsed > 2:
            summarized.append(submission.id)
        elif submission.id not in summarizing:
            summarizing.append(submission.id) 


# get new submissions
subreddit = r.get_subreddit('iama')
testing = r.get_submission(submission_id='2rtg51')
while True:
    for submission in subreddit.get_hot(limit=SUB_LIMIT):

        # filter out AMA requests
        if "[AMA Request]" in submission.title:
            continue

        # make sure not already finished
        if submission not in summarized and submission not in summarizing: 
            summarizing.append(submission)

        # summarizing the AMAs in summarizing[]
        summarize()
        
        sleep(SLEEP_TIME)


