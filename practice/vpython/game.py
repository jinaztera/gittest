Web VPython 3.2

import random

#볼 생성 함수
def ball_pos(a, b, c):
    return sphere(pos = vec(a, b, c))
    
#링 생성 함수
def ring_pos(a, b, c):
    return ring(axis = vector(0, 0, 1), radius = 1.5, thickness = 0.3, pos= vec(a, b, c))

ring_list = []
ball_list = []

#볼, 링 리스트에 담기
for i in range(-10, 11, 5) :
    for j in range(-10, 11, 5) :
        ring_list.append(ring_pos(i, j, 0))
        ball_list.append(ball_pos(i, j, 0))

for i in range(25) :
    ball_list[i].visible = False
    ring_list[i].visible = False

# 성공, 실패 체크
check_list = [text(text='Success', pos = vec(15, 2, 0)), text(text='Fail', pos = vec(15, -2, 0))]

def showSphere(evt):
    global loc
    loc = evt.pos

button(text = "공의 개수", bind = start)

def start():
    action
    
s1 = slider(min=5, max=25, step = 1, bind=f1)
print("공의 개수 설정 후 아무키를 누르면 게임이 시작됩니다.")

ev = scene.waitfor('keydown')

#슬라이더로 링의 개수 설정하기
def f1() :
    global ring_number
    ring_number = s1.value
    return ring_number
    
n = 1

n_text = text((text = "1 / 15"), pos = vec(-18, 10, 0))

success_num = 0
fail_num = 0

while n < 16 :    
    
    for i in range(f1()):
        ring_list[i].visible = True
      
    
    loc = vec(100, 100, 100)
    time = random.randint(1, 3) # 두더지 1 ~ 3초 동안 나와있기
    

    rate(1 / ( 3 * random.random()))
    
    check_list[0].color = color.black
    check_list[1].color = color.black
    
    # 두더지 랜덤 나오기
    r = random.randint(0, f1() - 1)
    ball_list[r].visible = True
            
    a = 0 
    for i in range(time * 100):
        a = a + 1 
        scene.bind('click', showSphere)

        if (ball_list[r].pos - loc).mag < 1 : # 볼의 위치와 마우스의 클릭위치의 거리가 1 이하일 때
            ball_list[r].visible = False
            print( a / 100, "초", "성공!")
            check_list[0].color = color.blue
            success_num += 1
            break
                
        if a == time * 100 : 
            check_list[1].color = color.red
            fail_num += 1
            print("실패!")
                    
        rate(100) # 0.01 초씩 체크하기
    
    ball_list[r].visible = False
    n = n + 1
    
    if n < 16 :
        n_text.visible = False
        n_text = text(text = str(n) + " / 15", pos = vec(-18, 10, 0))
    
    
print("success : " + str(success_num), "fail : " + str(fail_num))
    