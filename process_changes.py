"""
This is a program that will read in the changes_python.log file
and perform some analysis on it

Programmed by Andrew Doran-Sherlock in November 2017
"""

import pandas as pd
import collections as coll


def read_file(any_file):
    # use strip to strip out spaces and trim the line.
    data = [line.strip() for line in open(any_file, "r")]
    return data

def get_commits(data):
    sep = 72*"-"
    commits = []
    index = 0
    while index < len(data):
        try:
            # parse each of the commits and put them into a list of commits
            details = data[index + 1].split('|')
            # the author with spaces at end removed.
            commit = {"revision": details[0].strip(),
                "author": details[1].strip(),
                "date": details[2].strip().split(' ')[0],
                "time": details[2].strip().split(' ')[1],
                "number_of_lines": details[3].strip().split(' ')[0]
            }
            # add details to the list of commits.
            commits.append(commit)
            index = data.index(sep, index + 1)
        except IndexError:
            index = len(data)
    return commits

def save_commits(commits, any_file):
    my_file = open(any_file, "w")
    my_file.write("revision,author,date,time,number_of_lines\n")
    for commit in commits:
        my_file.write(commit["revision"]+","+commit["author"]+","+commit["date"]+","+commit["time"]+","+commit["number_of_lines"]+"\n")
    my_file.close()

if __name__ == "__main__":
    
    #open the file - and read all of the lines.
    changes_file = "changes_python.log"
    data = read_file(changes_file)
    #pull the details of the commits
    commits = get_commits(data)
    #save the cleaned commits into a csv file
    save_commits(commits,"changes.csv")
    
    #convert the commits into a dataframe
    commits = pd.DataFrame(data = commits)
    #get a list of the unique dates
    unique_dates = pd.unique(commits["date"])
    #get a list of the unique authors
    unique_authors = pd.unique(commits["author"])
    
    times = commits["time"]
    dates = commits["date"]
    list_of_authors = unique_authors.tolist()
    list_of_times = times.tolist()
    list_of_times.sort()
    rounded_times = []
    rounded_hours = []
    
    #round the times of the commits to the nearest hour
    for i in range(len(list_of_times)):
        if int(list_of_times[i][4:5]) < 30:
            rounded_hours.append(int(list_of_times[i][0:2]))
        else:
            rounded_hours.append(int(list_of_times[i][0:2]) + 1)
    rounded_hours = [int(x) for x in rounded_hours]

    for i in range(len(rounded_hours)):
        rounded_times.append(str(rounded_hours[i]) + ":00")
    

    #print a table of the times and the number of commits    
    print "Time        Commits"
    print
    for hour in pd.unique(rounded_times):
        count = 0
        for j in rounded_times:
            if hour == j:
                count = count + 1
        hour = str(hour)
        count = str(count)
        if len(hour) < 5:
            hour = "0" + hour
        print hour + " " * 10 + count
    
    print
    print
    print
    

    #print a table of the dates and the number of commits    
    print "  Date           Commits"
    print
    for date in pd.unique(dates):
        count = 0
        for j in dates:
            if date == j:
                count = count + 1
        print str(date) + " "*10 + str(count)
    
    
    #produce a histogram of the authors and the number of commits
    df = pd.DataFrame.from_dict(coll.Counter(commits["author"]), orient="index")
    ax = df.plot(kind='bar', title = 'No of entries per author', legend = False,
            figsize=(10,5))
    ax.set_xlabel('Users',fontsize=12)
    ax.set_ylabel('Frequency',fontsize=12)

