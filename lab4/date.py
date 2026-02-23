import datetime

today = datetime.datetime.now()
new_date = today - datetime.timedelta(days=5)

print(new_date)



import datetime

today = datetime.date.today()

yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)



import datetime

now = datetime.datetime.now()
no_micro = now.replace(microsecond=0)

print(no_micro)


import datetime

date1 = datetime.datetime(2026, 2, 23, 10, 0, 0)
date2 = datetime.datetime(2026, 2, 24, 10, 0, 0)

diff = date2 - date1
print(diff.total_seconds())