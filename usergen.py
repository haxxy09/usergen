import csv

reader = csv.DictReader(open("test_users.csv"))
list = []
for row in reader:
    print(row["username"])
