class Robot:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def move(self):
        print("이동")

    def stop(self):
        print("멈춤")

robot1 = Robot("멍멍이", 32)
robot2 = Robot("댕댕이", 20)

print(robot1.name)
print(robot2.age)
robot1.move()
robot2.stop()
