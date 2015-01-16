import praw
import pprint

r = praw.Reddit('More Music Bot by u/w4ngatang v 0.1.'
                'Url: https:https://github.com/W4ngatang/redditMusicBot')

already_done = []
songs = {}
temp = []
temp2 = []

subreddit = r.get_subreddit('listentothis')
for submission in subreddit.get_hot(limit=10):
        if "--" in submission.title:
                    temp = submission.title.split(" -- ")
                            temp2 = temp[1].split(" [")
                                    pprint.pprint(temp2[0] + " by " + temp[0])
                                        elif "-" in submission.title:
                                                temp = submission.title.split(" - ")
                                                        temp2 = temp[1].split(" [")
                                                                pprint.pprint(temp2[0] + " by " + temp[0])

