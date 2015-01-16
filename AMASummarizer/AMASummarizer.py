import praw
import pprint
import time

MAX_LEN = 10000                                         # max message length, set by reddit
RESPONSE_LIMIT = 25                                     # number of comments to pull at a time
SUB_LIMIT = 10                                          # number of submissions to pull at a time
SLEEP_TIME = 600                                        # amount of time to sleep
TIME_LIMIT = 9                                          # time in hours for end of AMA detection
MSG_BASE = "Question | Answer \n ----------|----------" # base for summarizing

r = praw.Reddit('AMA Summarizer by u/w4ngatang v 0.1.'
                'URL: https://github.com/W4ngatang/RedditBots')

r.login('AMASummaryBot', '9kSYpVcGV5h1HC31mpfj')
summarized = [] 
summarizing = {}

subreddit = r.get_subreddit('iama')
testing = r.get_submission(submission_id='2sl2uo')

# go through summarizing list and update, removing into summarized if detect AMA finished
def summarize():
    for submission in summarizing:

        # time variables to check when AMA has finished
        current = int(time.time())
        most_recent = -1 

        # create initial message, set up table
        msg = MSG_BASE 

        # first element in value list is last edited node        
        working = summarizing[submission][0]

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

                # if working node is NULL, add_comment
                # if new question is short enough, edit existing message, else post new message
                # post the existing msg and reset msg
                if working == 1:
#                    working = testing.add_comment(MSG_BASE + tmp) for testing
                    time.sleep(SLEEP_TIME)
                    working = submission.add_comment(MSG_BASE + tmp)
                elif len(working.body + tmp) < MAX_LEN:
                    working = working.edit(working.body + tmp)
                else:
                    time.sleep(SLEEP_TIME)
                    if working.is_root:
                        working = working.reply(MSG_BASE + tmp)
                    else:
                        parent_url = r.get_submission(working.link_url + working.parent_id[3:])
                        parent = parent_url[0] 
                        working = parent.reply(MSG_BASE + tmp)

                # keep track of latest submission time, for end of AMA detection
                elapsed = (current - response.created_utc) / 60 / 60 
                if elapsed < most_recent or most_recent == -1:
                    most_recent = elapsed

                # add to the list of comments tracked
                summarizing[submission].append(response)

        # update the latest comment to be working on for this submission
        summarizing[submission][0] = working

        # check if AMA has finished
        # roughly determined by latest from author to the AMA is older than TIME_LIMIT hrs
        if most_recent > TIME_LIMIT:
            del summarizing[submission] 
            summarized.append(submission)

# get new submissions
while True:
    for submission in subreddit.get_hot(limit=SUB_LIMIT):

        # filter out AMA requests
        if "[AMA Request]" in submission.title:
            continue

        # make sure not already finished and not currently working on
        if submission not in summarized and submission not in summarizing: 
            summarizing[submission] = []
            summarizing[submission].append(1) # reserve the first place for the root comment

        # summarizing the AMAs in summarizing[]
        summarize()
        
        time.sleep(SLEEP_TIME)


