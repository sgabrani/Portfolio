import sys
import json

get = sys.argv[1]
get = json.loads(get)
# get ={"timeline_posts":[{"content":"testing","created_at":"Fri, 14 Jul 2023 19:07:20 GMT","email":"manya@gmail.com","id":5,"name":"Manya"},{"content":"testing from curl","created_at":"Fri, 14 Jul 2023 03:41:05 GMT","email":"sahiti@gmail.com","id":3,"name":"SG"},{"content":"testing endpoint 2","created_at":"Fri, 14 Jul 2023 02:28:23 GMT","email":"sa@gmail.cpm","id":2,"name":"shreya"},{"content":"testing endpoint","created_at":"Fri, 14 Jul 2023 02:26:59 GMT","email":"sg@ucla.edu","id":1,"name":"sahiti"}]}
post = sys.argv[2]
post = json.loads(post)
# post = {"content":"testing","created_at":"Fri, 14 Jul 2023 19:07:20 GMT","email":"manya@gmail.com","id":5,"name":"Manya"}
if get["timeline_posts"][0]==post:
    print("The output matches :)")
else:
    print("the output does not match :(")
