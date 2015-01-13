import praw
import pprint
import time

MAX_LEN = 10000                                         # max message length, set by reddit
RESPONSE_LIMIT = 10                                     # number of comments to pull at a time
SUB_LIMIT = 10                                          # number of submissions to pull at a time
SLEEP_TIME = 120                                        # amount of time to sleep
TIME_LIMIT = 2                                          # time in hours for end of AMA detection
MSG_BASE = "Question | Answer \n ----------|----------" # base for summarizing

r = praw.Reddit('AMA Summarizer by u/w4ngatang v 0.1.'
                'URL: https://github.com/W4ngatang/RedditBots')

r.login('AMASummaryBot', '9kSYpVcGV5h1HC31mpfj')
summarized = [] 
summarizing = {}

# go through summarizing list and update, removing into summarized if detect AMA finished
def summarize():
    for submission in summarizing:

        # time variables to check when AMA has finished
        current = int(time.time())
        most_recent = None 

        # create initial message, set up table
        msg = MSG_BASE 
        
        # find root comment (if it's there)
        # if it has children, find which is the most recent to edit on
        root = summarizing[submission][0]
        working = root
        early_elapsed = (current_time - root.created_utc) / 60
        for reply in root.replies():
           elapsed = (current_time - reply.created_utc) / 60 
           if elapsed < early_elapsed: #and (belongs to bot):
               working = reply
               early_elapsed = elapsed 

        # get all the responses posted by AMA author
        author = r.get_redditor(submission.author)
        responses = author.get_comments(limit = RESPONSE_LIMIT)
        for response in responses:

            # if the response is for the AMA
            if response.submission == submission and response not in summarizing[submission]:

                # get the comment's parent (the question)
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
                if len(working.body + tmp) < MAX_LEN:
#                    testing.add_comment(msg) if root == None else root.reply(msg)
                    testing.edit(working.body + tmp)
                else:
                    msg = msg + tmp 

                # keep track of latest submission time, for end of AMA detection
                elapsed = (current_time - recent.created_utc) / 60 / 60 
                if elapsed < most_recent or most_recent == None:
                    most_recent = elapsed

                # add to the list of comments tracked
                summarizing[submission].append(response)

        # post the message
        if len(msg) > len(MSG_BASE): 
            testing.add_comment(msg) if root == None else root.reply(msg)

        # check if AMA has finished
        # roughly determined by latest from author to the AMA is older than 2 hrs
        if most_recent > TIME_LIMIT:
            del summarizing[submission] 
            summarized.add(submission)


# get new submissions
subreddit = r.get_subreddit('iama')
testing = r.get_submission(submission_id='2rtg51')
while True:
    for submission in subreddit.get_hot(limit=SUB_LIMIT):

        # filter out AMA requests
        if "[AMA Request]" in submission.title:
            continue

        # make sure not already finished and not currently working on
        if submission not in summarized and submission not in summarizing: 
            summarizing[submission] = []
            summarizing[submission][0] = None # reserve the first place for the root comment

        # summarizing the AMAs in summarizing[]
        summarize()
        
        sleep(SLEEP_TIME)


