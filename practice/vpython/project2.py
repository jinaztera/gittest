from vpython import *


import random


def ball_pos(a, b, c):
    return sphere(pos = vec(a, b, c))
    
def ring_pos(a, b, c):
    return ring(axis = vector(0, 0, 1), radius = 1.5, thickness = 0.3, pos= vec(a, b, c))

ring_pos(-5, -5, 0)
ring_pos(-5, 0, 0)
ring_pos(-5, 5, 0)
ring_pos(0, -5, 0)
ring_pos(0, 0, 0)
ring_pos(0, 5, 0)
ring_pos(5, -5, 0)
ring_pos(5, 0, 0)
ring_pos(5, 5, 0)



ball_list = [ball_pos(-5, -5, 0), ball_pos(-5, 0, 0), ball_pos(-5, 5, 0), ball_pos(0, -5, 0), ball_pos(0, 0, 0), ball_pos(0, 5, 0), ball_pos(5, -5, 0), ball_pos(5, 0, 0), ball_pos(5, 5, 0)]

for i in range(9) :
    ball_list[i].visible = False

print(5 * random.random())
print(random.randint(1, 9))

loc = vec(0, 0, 0)

check_list = [text(text='Success', pos = vec(10, 2, 0)), text(text='Fail', pos = vec(10, -2, 0))]

#check.color = color.red
#check

def showSphere(evt):
    global loc
    loc = evt.pos
    print(loc)

while True :    
    
    time = random.randint(1, 3)
    
    rate(1 / ( 3 * random.random()))
    check_list[0].color = color.black
    check_list[1].color = color.black
    
    r = random.randint(0, 8)
    ball_list[r].visible = True
    
    
#    rate(0.5)
    a = 0
    for i in range(time * 10):
#        print(i)
        a = a + 1
        scene.bind('click', showSphere)
        if (ball_list[r].pos - loc).mag < 1 :
            ball_list[r].visible = False
            print(a / 10)
            check_list[0].color = color.blue
            break
        
        if a == time * 10 :
#            print("hello")
            check_list[1].color = color.red
            
        
        rate(10)
        
    
    
    ball_list[r].visible = False