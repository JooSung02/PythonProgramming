def calc(v1, v2, op) :
    result = 0
    
    if op == '+' :
        result = v1 + v2
    elif op == '-' :
        result = v1 - v2
    elif op == ' *' :
        result = v1 * v2
    elif op == '/' :
        result = v1 / v2

    
    return result

res = 0
var1 ,var2, operation = 0, 0, ""

oper = input("계산을 입력 : ")
var1 = int(input("첫번 째 수 입력"))
var2 = int(input("두번 째 수 입력"))

res = calc(var1, var2, operation)
print("계산기 : %d %s %d = %d" %(var1, operation, var2, res))