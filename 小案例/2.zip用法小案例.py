usernames = ["alice123", "bob456", "charlie789"]
passwords = ["pass1", "pass2", "pass3"]
user_input = [("alice123", "pass1"), ("bob456", "wrong")]

def authenticate(username, password):
    credentials = dict(zip(usernames, passwords))
    print("credentials:", credentials)
    return credentials.get(username) == password

for u, p in user_input:
    print(f"{u}: {'登录成功' if authenticate(u, p) else '登录失败'}")