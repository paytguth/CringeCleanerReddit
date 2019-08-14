
import praw, sys, re, getpass
from multiprocessing import Process
from datetime import datetime
# python redditbot.py username client_id client_secret


reddit = praw.Reddit(
    client_id = sys.argv[2],
    client_secret = sys.argv[3],
    username = sys.argv[1],
    password = getpass.getpass("Password: "),
    user_agent = 'linux:Reddit Cleaner:1.0 (by /u/espresso_snake)'

)


# Prints comment body and stats to console
# Arg type: PRAW Comment object
def displayComment(comment) :
    print("****************************************************************************")
    print("(" + str(comment.score)
    + " karma) r/"
    + comment.subreddit.display_name
    + " "
    + str(datetime.fromtimestamp(comment.created_utc)))
    print(comment.body)


# Overwrites and deletes comments from user profile
# Arg type: List of PRAW Comment objects
def deleteComments(commentList) :
    for comment in commentList :
        comment.edit("*[deleted]*")
        comment.delete()


# Searches for and deletes all user comments in user specified subreddit
# Arg type: Username String
def searchCommentsBySubreddit(username) :
    commentList = []
    subredditKeyword = str(input("Please enter name of subreddit you'd like to delete all comments from\n")).lower()
    print("Showing all comments from subreddit \'r/" + subredditKeyword + "\'")

    for comment in reddit.redditor(username).comments.top(limit=None) :
        subredditName = str(comment.subreddit.display_name).lower()
        if subredditKeyword == subredditName:
            displayComment(comment)
            commentList.append(comment)

    if (commentList != []) :
        deleteOrNot = str(input("Delete all comments shown? (y/n) ")).lower()
        if (deleteOrNot == "y") :
            deleteComments(commentList)
    else :
        print("No comments from " + username + " found in \'r/" + subredditKeyword + "\'")


# Searches for and deletes all user comments that contain user specified keyword
# Arg type: Username String
def searchCommentsByKeyword(username) :
    commentList = []

    keyword = str(input("Please enter keyword you'd like to delete all comments containing\n"))
    print("Showing all comments containing keyword \'" + keyword + "\'")

    for comment in reddit.redditor(username).comments.top(limit=None) :
        # Searches comment body for keyword. not case sensitive. Regex
        expression = r"\b" + re.escape(keyword) + r"\b"
        match = re.search(expression, comment.body, re.I)
        if (match) :
            displayComment(comment)
            commentList.append(comment)

    if (commentList != []) :
        deleteOrNot = str(input("Delete all comments shown? (y/n) ")).lower()
        if (deleteOrNot == "y") :
            deleteComments(commentList)
    else :
        print("No comments containing keyword \'" + keyword + "\'" + " were found")


def main() :
    username = sys.argv[1]
    reddit.read_only = False

    # Intro
    subOrKeyword = input("Enter s to delete comment by subreddit, and k to delete comment by keyword\n")

    # Deleting by subreddit
    if (subOrKeyword == "s") :
        searchCommentsBySubreddit(username)

    # Deleting by comment keyword
    elif (subOrKeyword == "k") :
        searchCommentsByKeyword(username)

    # Invalid option
    else :
        print("Sorry, what was typed was not a valid option")



if __name__ == "__main__":
    main()
