import random

# Fonction de tri par insertion
def tri_insertion(arr):

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


if __name__ == "__main__":

    random_list = [random.randint(0, 100) for _ in range(10)]
    print("Liste initiale :", random_list)

    tri_insertion(random_list)
    print("Liste triée :", random_list)