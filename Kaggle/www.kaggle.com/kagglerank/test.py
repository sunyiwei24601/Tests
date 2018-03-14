usernames=[]
start=1
end=1935
import csv
with open("kaggle_competition_id.csv", newline='', encoding='utf-8') as f:
    c = csv.reader(f, delimiter=' ', quotechar='|')
    n = 0
    for row in c:

        if (n >= start and n <= end):
            usernames.append(row[0])
            if row[0] == '3136':
                print(n)
        elif(n>end):
            break
        n += 1

