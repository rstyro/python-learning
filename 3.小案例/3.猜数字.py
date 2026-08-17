import random

def guessGame():
    # 随机数，1-100
    target = random.randint(1, 100)
    count = 5  # 最多猜5次

    print("=" * 30)
    print("🎉 欢迎来到猜数字游戏 🎉")

    while count > 0:
        try:
            guess = int(input(f"你还有{count}次机会，请输入数字："))
            if guess == target:
                print("恭喜你，猜对了！")
                break
            elif guess < target:
                print("猜小了！")
            else:
                print("猜大了！")
            count -= 1
        except ValueError:
            print("输入错误！只能输入有效数字，请重新输入")

    if count == 0:
        print(f"游戏结束！正确数字是：{target}")

if __name__ == '__main__':
    guessGame()