import numpy as np

# Sigmoid and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Training data (XOR problem)
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array([
    [0],
    [1],
    [1],
    [0]
])

# Seed for reproducibility
np.random.seed(42)

# Initialize weights
input_size = 2
hidden_size = 2
output_size = 1

W1 = np.random.uniform(-1, 1, (input_size, hidden_size))
b1 = np.zeros((1, hidden_size))
W2 = np.random.uniform(-1, 1, (hidden_size, output_size))
b2 = np.zeros((1, output_size))

print("W1", W1)
print("b1", b1)
print("W2", W2)
print("b2", b2)

# Training loop
epochs = 10000
lr = 0.1

for epoch in range(epochs):
    # Forward pass
    z1 = X @ W1 + b1
    print("z1", z1)
    a1 = sigmoid(z1)
    print("a1", a1)

    z2 = a1 @ W2 + b2
    print("z2", z2)
    a2 = sigmoid(z2)
    print("a2", a2)

    # Loss (mean squared error)
    loss = np.mean((y - a2) ** 2)
    print("loss", loss)
    
    # Backpropagation
    d_a2 = (a2 - y)
    d_z2 = d_a2 * sigmoid_derivative(a2)

    d_W2 = a1.T @ d_z2
    d_b2 = np.sum(d_z2, axis=0, keepdims=True)

    d_a1 = d_z2 @ W2.T
    d_z1 = d_a1 * sigmoid_derivative(a1)

    d_W1 = X.T @ d_z1
    d_b1 = np.sum(d_z1, axis=0, keepdims=True)

    # Update weights and biases
    W2 -= lr * d_W2
    b2 -= lr * d_b2
    W1 -= lr * d_W1
    b1 -= lr * d_b1

    # Print every 1000 epochs
    if epoch % 1000 == 0:
        print(f"Epoch {epoch}, Loss: {loss:.4f}")

# Final predictions
predictions = sigmoid(X @ W1 + b1) @ W2 + b2
print("\nFinal Output (after sigmoid):")
print(sigmoid(predictions))
