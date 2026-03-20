# 1.4 
sum_numbers = 0
count = 0

num = int(input("Введите число:"))

while num != 0:
    sum_numbers += num 
    count += 1
    num = int(input("Введите число:"))
    
print("Сумма чисел: ", sum_numbers)
print("Количество чисел: ", count)