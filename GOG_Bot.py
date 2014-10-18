#Libraries needed for working
from __future__ import print_function
import praw     #External lib, needs easy_install
import ntplib   #External lib
import time 
import datetime
from   time import ctime

def login(r):
    username = 'GOG_Bot'
    password = raw_input("Password:")
    r.login(username,password)
    print("\nLogged in.")
    return r

def get_date():
    x = ntplib.NTPClient()
    response = x.request('pool.ntp.org')
    now = datetime.datetime.strptime(ctime(response.tx_time), "%a %b %d %H:%M:%S %Y")
    date = now.now().timetuple().tm_yday

    return date

def get_age(thread):
    age = str(thread.selftext.split('\n',1)[0])
    age = age.replace("[](/", "")
    age = age.replace(")", "")
    age = int(age)

    return age

def fill_list(file_name):
    list_ = []

    temp = open(file_name, 'r')

    for line in temp:
        list_.append(line)

    list_[0].replace("\\n","")

    return list_

def get_gog_submissions(r):
    print("\nGetting /r/gog's submissions.")

    subreddit = r.get_subreddit('gog')
    submissions = subreddit.get_new(limit=100)
    return submissions

def submit_thread(thread, r, subreddit, age, date):
    body = thread.selftext
    body = body.replace(str(age), str(date))
    submission = r.submit(subreddit, thread.title, body)
    submission.sticky()
    submission.set_flair(thread.link_flair_css_class)

def check_submissions(submissions,already_checked,thread_titles,date,r):
    for thread in submissions:
        if thread.title in thread_titles and thread.title not in already_checked:
            age = get_age(thread)
            print("\nThread:",thread.title)
            if (date - age) >= 7:     
                submit_thread(thread, r, 'gog', age, date)
                already_checked.append(thread.title)
                print("New thread posted")
            else:
                print("Thread is too young, age:", date-age)
                already_checked.append(thread.title)

    return already_checked

def main():
    print("###GOG Bot###")

    already_checked = []
    #thread_titles = fill_list('titles.txt')
    thread_titles = ["What have you been playing this week?","New Member Monday!"]

    r = praw.Reddit(user_agent='GOG_Bot_by_Matthew94')
    r = login(r)

    while(1):
        date = get_date()

        submissions = get_gog_submissions(r)
        already_checked = check_submissions(submissions,
                                            already_checked,
                                            thread_titles,
                                            date,
                                            r)
        print("\nSleeping for an hour")
        time.sleep(3600)

#Runs the program
main()