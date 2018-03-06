import csv
with open("kaggle_username.csv",newline='',encoding='utf-8') as f:
    c=csv.reader(f,delimiter=' ', quotechar='|')
    n=0
    for row in c:
        print(row[0][4:-3])
        n+=1
        if n>20:
            break
