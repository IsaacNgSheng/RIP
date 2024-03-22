

def tri_a_bulle(t):
    for i in range(len(t)):
        for j in range(i-1):
            if t[j] > t[j + 1]:
                t[j], t[j + 1] = t[j - 1], t[j+1]


if __name__ == "__main__":

    list = [3, 1, 2, 5, 4]
    print("Liste initiale :", list)

    tri_a_bulle(list)

    print("Liste triée :", list)