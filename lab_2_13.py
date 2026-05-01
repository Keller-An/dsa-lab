a = input("Введите строку: ")
start = -1
end = -1 

for i in range(len(a)):
    if a[i] == "(":
        start = i
    elif a[i] == ")":
        end = i
        
if start != -1 and end != -1 and start < end:
    for i in range(start + 1, end):
        print(a[i], end="")
else:
    print("Скобки в тексте не найдены")