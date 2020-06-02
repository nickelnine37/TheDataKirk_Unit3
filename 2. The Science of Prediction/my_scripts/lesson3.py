import numpy as np
import matplotlib.pyplot as plt
from ipywidgets.widgets import interact
from scipy.stats import chi2
from sklearn.utils import shuffle

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


X, y = shuffle(*_gen_data(500, 300, seed=2), random_state=0)

    
    