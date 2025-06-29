import numpy as np

input_size = 2
hidden_size = 2
output_size = 1

a = [[1,2,3], 
     [4, 5, 6]]
b = [
    [10, 12, 13], 
    [21, 22, 23],
    [31, 32, 33]
   ]

c = [
    [10, 11],
    [20, 21],
    [30, 31]
]

x = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array(
    [[4, 5], [1, 2]]
)


W1 = np.random.uniform(-1, 1, (input_size, hidden_size))
print("W1", W1)

# print(x @ W1)
# print("a", a)
# print("b", b)
# print("c", c)
# print("W1", W1)
print(np.dot(a, c))
