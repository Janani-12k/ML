import numpy as np

class CandidateElimination:
    def __init__(self, num_features):
        self.num_features = num_features
        self.S = [np.zeros(num_features, dtype=int)]
        self.G = [np.ones(num_features, dtype=int)]

    def fit(self, X, y):
        for i in range(len(X)):
            if y[i] == 1:  # Positive example
                self.remove_inconsistent_G(X[i])
                self.generalize_S(X[i])
            else:  # Negative example
                self.remove_inconsistent_S(X[i])
                self.specialize_G(X[i])

    def remove_inconsistent_G(self, x):
        self.G = [g for g in self.G if np.all(g >= x)]

    def generalize_S(self, x):
        S_new = []
        for s in self.S:
            for i in range(len(s)):
                if s[i] != x[i]:
                    s_new = np.copy(s)
                    s_new[i] = -1  # -1 indicates a variable can take any value
                    S_new.append(s_new)
        self.S = S_new

    def remove_inconsistent_S(self, x):
        self.S = [s for s in self.S if not np.all(s >= x)]

    def specialize_G(self, x):
        G_new = []
        for g in self.G:
            for i in range(len(g)):
                if g[i] == 1 and x[i] != 1:
                    g_new = np.copy(g)
                    g_new[i] = 0
                    G_new.append(g_new)
        self.G = G_new

    def get_hypotheses(self):
        return self.S, self.G

# Example usage
X = np.array([
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
    [0, 0, 1]
])
y = np.array([1, 0, 1, 0])  # 1 for positive, 0 for negative

ce = CandidateElimination(num_features=X.shape[1])
ce.fit(X, y)
S_hypotheses, G_hypotheses = ce.get_hypotheses()

print("Final S Hypotheses:")
for s in S_hypotheses:
    print(s)

print("\nFinal G Hypotheses:")
for g in G_hypotheses:
    print(g)
