a = int(input())
b = int(input())
c = int(input())

D = b**2 - 4 * a * c
if D < 0:
    print("Корней нет")
else:
    x1 = (-b + D**0.5) / (2 * a)
    x2 = (-b - D**0.5) / (2 * a)
    if x1 == x2:
        print("Корень уравнения:", x1)
    else:
        print("Корни уравнения:", x1, x2)