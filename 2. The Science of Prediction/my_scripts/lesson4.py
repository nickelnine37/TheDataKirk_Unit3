import numpy as np
import matplotlib.pyplot as plt
from ipywidgets.widgets import interact
from scipy.stats import chi2
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import matplotlib

import warnings

warnings.filterwarnings("ignore", message="Numerical issues were encountered")

def make_graph_1():
    
    global w, t
    
    np.random.seed(11)
    fig, ax = plt.subplots()
    
    
    n_dogs = 70
    n_cats = 50
    
    X, y = _gen_data(n_dogs, n_cats)

    ax.scatter(X[:n_dogs, 0], X[:n_dogs, 1], label='Dogs', alpha=0.6)
    ax.scatter(X[n_dogs:, 0], X[n_dogs:, 1], label='Cats', alpha=0.6)
    
    plt.legend()
    plt.xlabel('Weight (kg)')
    plt.ylabel('Tail length (cm)')
    
    w, t = 0, 0
    point,  = plt.plot([55], [22], marker='o', linewidth=0, color='#1f77b4', alpha=0.6)
    colors = ['#ff7f0e', '#1f77b4']
    
    data = np.zeros((n_cats + n_dogs, 3))
    data[:, :2] = X
    data[:, 2] = y
    
    def get_dists(x, y):
        dists = ((data[:, 0] - x) ** 2 + (data[:, 1] - y) ** 2) ** 0.5
        sortd = np.argsort(dists)[:5]
        return data[sortd, :]
    
    lines = []
    
    d0 = get_dists(55, 22)
    lines = [plt.plot([22, d0[i, 0]], [55, d0[i, 1]], color=colors[int(d0[i, 2])], alpha=0.3)[0] for i in range(5)]
        
    def update():
        global w, t
        
        new_dists = get_dists(w, t)
        for i, line in enumerate(lines):
            line.set_xdata([w, new_dists[i, 0]])
            line.set_ydata([t, new_dists[i, 1]])
            line.set_color(colors[int(new_dists[i, 2])])
            
        if new_dists[:, 2].sum() > 2.5:
            point.set_color(colors[1])
            ax.set_title('Predict a dog')
        else:
            point.set_color(colors[0])
            ax.set_title('Predict a cat')
    
    def update_weight(weight=15.5):
        global w, t
        
        w = weight
        point.set_xdata([weight])
        update()

    def update_tail(tail=47):
        global w, t
        
        t = tail
        point.set_ydata([tail])    
        update()

    interact(update_weight, weight=(0, 70, 0.01))
    interact(update_tail,   tail=(10, 70, 0.01))
    
    
def _gen_data(n_dogs, n_cats, seed=0):
    
    np.random.seed(seed)
    X = np.zeros((n_dogs + n_cats, 2))
    X[:n_dogs, 0] = chi2.rvs(df=5, loc=0, scale=5, size=n_dogs)
    X[:n_dogs, 1] = np.abs((X[:n_dogs, 0] ** 0.8 + np.random.normal(10, 10, n_dogs))/ 1.2 + 12) ** 1
    X[n_dogs:, 0] = 0.45 * (3 + np.random.gamma(7.5, 1.5, n_cats))
    X[n_dogs:, 1] = np.random.normal(35, 3.5, n_cats)
    y = np.concatenate([np.ones(n_dogs), np.zeros(n_cats)])
    
    return X, y


def make_graph_2():
        
    np.random.seed(11)
    fig, ax = plt.subplots()
    
    n_dogs = 70
    n_cats = 50
    
    X, y = _gen_data(n_dogs, n_cats)
    
    classifier = KNeighborsClassifier(n_neighbors=5)

    classifier.fit(X, y)

    ax.scatter(X[:n_dogs, 0], X[:n_dogs, 1], label='Dogs', alpha=0.6)
    ax.scatter(X[n_dogs:, 0], X[n_dogs:, 1], label='Cats', alpha=0.6)
    
    x_space = np.linspace(*ax.get_xlim(), 100)
    y_space = np.linspace(*ax.get_ylim(), 100)
    
    XX, Y = np.meshgrid(x_space, y_space)
    X = np.vstack([XX.reshape(-1), Y.reshape(-1)]).T
    
    plt.legend()
    plt.xlabel('Weight (kg)')
    plt.ylabel('Tail length (cm)')

    out = classifier.predict(X)
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        ax.contour(XX, Y, out.reshape(100, 100), levels=0, ls='--')
        
    for item in ax.get_children():
        if isinstance(item, matplotlib.collections.LineCollection):
            item.set_linewidth([1])
            item.set_color('k')
            item.set_alpha(0.6)
    
    
    ax.text(-1.6, 48, 'Predict a cat')
    ax.text(15, 44, 'Predict a dog')
    
    
def plot_decision_boundary(X, y, classifier):
    
    fig, ax = plt.subplots()
    
    classifier.fit(X, y)
    
    ax.scatter(X[y == 1, 0], X[y == 1, 1], label='Class 1', alpha=0.6)
    ax.scatter(X[y == 0, 0], X[y == 0, 1], label='Class 0', alpha=0.6)
    
    x_space = np.linspace(*ax.get_xlim(), 100)
    y_space = np.linspace(*ax.get_ylim(), 100)
    
    XX, YY = np.meshgrid(x_space, y_space)
    out = classifier.predict(np.vstack([XX.reshape(-1), YY.reshape(-1)]).T)

    plt.legend()
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        ax.contour(XX, YY, out.reshape(100, 100), levels=0, ls='--')
        
    for item in ax.get_children():
        if isinstance(item, matplotlib.collections.LineCollection):
            item.set_linewidth([1])
            item.set_color('k')
            item.set_alpha(0.6)
    
    
def find_best_decision_bondary():
    
    np.random.seed(0)
    fig, ax = plt.subplots()
   
    ax.set_aspect('equal')

    x1 = np.random.normal(2, 1.5, 25)
    x2 = np.random.normal(-2, 1.5, 25)
    y1 = np.random.normal(2, 1.5, 25)
    y2 = np.random.normal(-2, 1.5, 25)

    ax.scatter(x1, y1, alpha=0.6)
    ax.scatter(x2, y2, alpha=0.6)
    
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    ax.set_title("Title x")
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    
    ax.set_xticks([])
    ax.set_yticks([])
    
    x = np.linspace(-5, 5, 100)
    line, = ax.plot(x, x, lw=1, ls='--', color='k', alpha=0.4)
    
    class Line:
        
        def __init__(self, a, b):
            self.a = a
            self.b = b
            
            self.m = None
            self.fill1 = None
            self.fill2 = None
            
            self.n = len(x1) + len(x2)
            
            self.set_y()
            
        def set_y(self):
            
            self.m = np.tan(self.b * np.pi / 180)
            self.y = self.a + self.m * x
            line.set_ydata(self.y)
            
            if self.fill1 is not None:
                self.fill1.remove()
                self.fill2.remove()
                
            if self.b > 90 or self.b < -90:
                self.fill1 = ax.fill_between(x, -5, self.y, color='#1f77b4', alpha=0.3)
                self.fill2 = ax.fill_between(x, self.y, 5, color='#ff7f0e', alpha=0.3)
            else:
                self.fill1 = ax.fill_between(x, -5, self.y, color='#ff7f0e', alpha=0.3)
                self.fill2 = ax.fill_between(x, self.y, 5, color='#1f77b4', alpha=0.3)
                
        def accuracy(self):
            if self.b > 90 or self.b < -90:
                return ((y2 > self.a + self.m * x2).sum() + (y1 < self.a + self.m * x1).sum()) / self.n
            else:
                return ((y1 > self.a + self.m * x1).sum() + (y2 < self.a + self.m * x2).sum()) / self.n
            
        def set_title(self, title):
            ax.set_title(title)
            
    theLine = Line(1, 45)
    
    def update():
        theLine.set_y()
        ac = f'accuracy = {theLine.accuracy() * 100:.0f}%'
        theLine.set_title(ac)

    def update_a(a=0):
        theLine.a = a
        update()

    def update_b(b=45):
        theLine.b = b
        update()
    
    interact(update_a, a=(-10, 10, 0.001))
    interact(update_b, b=(-180, 180, 0.01))
    
    plt.tight_layout()
    
    
def find_best_decision_bondary2():
    
    np.random.seed(0)
    fig, ax = plt.subplots()
   
    ax.set_aspect('equal')
    
    x1 = np.random.normal(2, 2.1, 25)
    x2 = np.random.normal(-2, 2.1, 25)
    y1 = np.random.normal(2, 2.1, 25)
    y2 = np.random.normal(-2, 2.1, 25)

    ax.scatter(x1, y1, alpha=0.6)
    ax.scatter(x2, y2, alpha=0.6)
    
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    ax.set_title("Title x")
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    
    ax.set_xticks([])
    ax.set_yticks([])
    
    x = np.linspace(-5, 5, 100)
    line, = ax.plot(x, x, lw=1, ls='--', color='k', alpha=0.4)
    
    class Line:
        
        def __init__(self, a, b):
            self.a = a
            self.b = b
            
            self.m = None
            self.fill1 = None
            self.fill2 = None
            
            self.n = len(x1) + len(x2)
            
            self.set_y()
            
        def set_y(self):
            
            self.m = np.tan(self.b * np.pi / 180)
            self.y = self.a + self.m * x
            line.set_ydata(self.y)
            
            if self.fill1 is not None:
                self.fill1.remove()
                self.fill2.remove()
                
            if self.b > 90 or self.b < -90:
                self.fill1 = ax.fill_between(x, -5, self.y, color='#1f77b4', alpha=0.3)
                self.fill2 = ax.fill_between(x, self.y, 5, color='#ff7f0e', alpha=0.3)
            else:
                self.fill1 = ax.fill_between(x, -5, self.y, color='#ff7f0e', alpha=0.3)
                self.fill2 = ax.fill_between(x, self.y, 5, color='#1f77b4', alpha=0.3)
                
        def accuracy(self):
            if self.b > 90 or self.b < -90:
                return ((y2 > self.a + self.m * x2).sum() + (y1 < self.a + self.m * x1).sum()) / self.n
            else:
                return ((y1 > self.a + self.m * x1).sum() + (y2 < self.a + self.m * x2).sum()) / self.n
            
        def set_title(self, title):
            ax.set_title(title)
            
    theLine = Line(1, 45)
    
    def update():
        theLine.set_y()
        ac = f'accuracy = {theLine.accuracy() * 100:.0f}%'
        theLine.set_title(ac)

    def update_a(a=0):
        theLine.a = a
        update()

    def update_b(b=45):
        theLine.b = b
        update()
    
    interact(update_a, a=(-10, 10, 0.001))
    interact(update_b, b=(-180, 180, 0.01))
    
    plt.tight_layout()
        
        
        
def graded_decision_boundary():
    
    fig, ax = plt.subplots()
    np.random.seed(0)
    
    x1 = np.random.normal(2, 2.1, 25)
    x2 = np.random.normal(-2, 2.1, 25)
    y1 = np.random.normal(2, 2.1, 25)
    y2 = np.random.normal(-2, 2.1, 25)

    ax.scatter(x1, y1, alpha=0.6)
    ax.scatter(x2, y2, alpha=0.6)
    
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    
    ax.set_aspect('equal')
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    
    x = np.linspace(-5, 5, 250)
    
    y = 1.67 + np.tan(-32.7 * np.pi / 180) * x
    
    plt.plot(x, y, color='k', ls='--', alpha=0.4, lw=1)
    
    s = 0.3
    
    fills1 = [ax.fill_between(x, y + i / 4, y + (i + 1) / 4, alpha= 1.8 / (1 + np.exp(-s * i / 4)) - 0.88, color='#1f77b4', lw=0.01) for i in range(40)]
    fills2 = [ax.fill_between(x, y - i / 4, y - (i + 1) / 4, alpha= 1.8 / (1 + np.exp(-s * i / 4)) - 0.88, color='#ff7f0e', lw=0.01) for i in range(40)]

    
def sigmoid():
    
    np.random.seed(0)
    fig, ax = plt.subplots()
   
    plt.xlabel('Distance from the boundary')
    plt.ylabel('Probability of being blue')
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.1, 1.1)
    
    x = np.linspace(-5, 5, 300)
    
    def f(sigma):
        return 1 / (1 + np.exp(- sigma * x))
    
    line, = ax.plot(x, f(1), lw=1, color='k', alpha=0.6)

    def update_s(s=1):
        line.set_ydata(f(s))
    interact(update_s, s=(0, 10, 0.01))
    
    plt.tight_layout()
        
    
np.random.seed(11)
X, y = _gen_data(70, 50)
