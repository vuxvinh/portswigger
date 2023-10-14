username = ["carlos"]

cnt = 1
for i in range (1,198):
    if (cnt%2==0):
        username.append('wiener')
    else:
        username.append('carlos')
    cnt+=1

for x in username:
    print(x)

# print(username)