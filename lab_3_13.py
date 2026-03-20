import random

n = int(input("Введите количество элементов массива: "))
arr = []

for i in range(n):
    arr.append(random.randint(0, 50))

print("Сгенерированный массив:", arr)

# поиск индексов повторяющихся элементов
indexes = []
for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
        if arr[i] == arr[j]:
            if i not in indexes:
                indexes.append(i)
            if j not in indexes:
                indexes.append(j)

if len(indexes) > 0:
    print("Индексы повторяющихся элементов:", indexes)
else:
    print("Повторяющихся элементов нет")

# замена элементов меньше 15
for i in range(len(arr)):
    if arr[i] < 15:
        arr[i] = arr[i] * 2

print("Полученный массив:", arr)

