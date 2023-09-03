
import pandas as pd

# 데이터프레임 생성
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emily'],
    'Age': [25, 32, 18, 47, 33],
    'City': ['Austin', 'Dallas', 'Chicago', 'Austin', 'Dallas']
})

# 출력
print(df)
df


# 계산기 코드를 작성해줘


def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

print("산술 연산을 선택하십시오.")
print("1. 덧셈")
print("2. 뺄셈")
print("3. 곱셈")
print("4. 나눗셈")

choice = input("선택(1/2/3/4): ")

num1 = float(input("첫 번째 숫자를 입력하십시오: "))
num2 = float(input("두 번째 숫자를 입력하십시오: "))

if choice == '1':
    print(num1,"+",num2,"=", add(num1,num2))

elif choice == '2':
    print(num1,"-",num2,"=", subtract(num1,num2))

elif choice == '3':
    print(num1,"*",num2,"=", multiply(num1,num2))

elif choice == '4':
    print(num1,"/",num2,"=", divide(num1,num2))
    
else:
    print("잘못된 입력") 
