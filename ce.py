class CandidateElimination:
    def __init__(self, num_features):
        self.num_features = num_features
        self.S = [{('?') for _ in range(num_features)}]  # Start with the most general hypothesis
        self.G = [{('0') for _ in range(num_features)}]  # Start with the most specific hypothesis

    def fit(self, X, y):
        for i in range(len(X)):
            x = X[i]
            if y[i] == 1:  # Positive example
                self.remove_inconsistent_G(x)
                self.generalize_S(x)
            else:  # Negative example
                self.remove_inconsistent_S(x)
                self.specialize_G(x)

    def remove_inconsistent_G(self, x):
        self.G = [g for g in self.G if not any([self.is_consistent(x, h) for h in g])]

    def is_consistent(self, x, h):
        return all([h[i] == '?' or h[i] == x[i] for i in range(self.num_features)])

    def generalize_S(self, x):
        S_new = []
        for s in self.S:
            for i in range(self.num_features):
                if s[i] == '?':
                    continue
                if s[i] != x[i]:
                    s_new = list(s)
                    s_new[i] = '?'
                    S_new.append(set(s_new))
            S_new.append(s)
        self.S = S_new

    def remove_inconsistent_S(self, x):
        self.S = [s for s in self.S if self.is_consistent(x, s)]

    def specialize_G(self, x):
        G_new = []
        for g in self.G:
            for i in range(self.num_features):
                if g[i] != '0' and g[i] != x[i]:
                    g_new = list(g)
                    g_new[i] = '0'
                    G_new.append(set(g_new))
            G_new.append(g)
        self.G = G_new

    def get_hypotheses(self):
        return self.S, self.G

# Example usage
X = [
    ('Sunny', 'Warm', 'Normal', 'Strong', 'Warm', 'Same'),
    ('Sunny', 'Warm', 'High', 'Strong', 'Warm', 'Same'),
    ('Rainy', 'Cold', 'High', 'Weak', 'Warm', 'Change'),
    ('Sunny', 'Warm', 'High', 'Strong', 'Cool', 'Change')
]
y = [1, 1, 0, 1]  # 1 for positive, 0 for negative

ce = CandidateElimination(num_features=len(X[0]))
ce.fit(X, y)
S_hypotheses, G_hypotheses = ce.get_hypotheses()

print("Final S Hypotheses:")
for s in S_hypotheses:
    print(s)

print("\nFinal G Hypotheses:")
for g in G_hypotheses:
    print(g)
