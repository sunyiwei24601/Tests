import csv
with open('Zhihu_Live.csv',newline='',encoding="utf-8") as f:
    reader=csv.DictReader(f)
    n=1
    for row in reader:
        print(row)
        n+=1
    print(n)