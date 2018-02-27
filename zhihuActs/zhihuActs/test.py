import json
with open("unfinished_url.txt") as f:
    j=json.load(f)
n=0
finished=0
for i in j:
    n+=1
    if not j[i]:
        finished+=1


print(n)
print(finished)