import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets.widgets import interact
from mpl_toolkits.mplot3d import Axes3D



def make_graph_1():
    
    np.random.seed(0)
    
    weight_dogs = 0.45 * (np.random.gamma(7.5, 10, 50))
    weight_cats = 0.45 * (3 + np.random.gamma(7.5, 1, 50))
    
    tail_cats = np.random.normal(45, 1.5, 50)
    tail_dogs = weight_dogs + np.random.normal(10, 10, 50)
    
    plt.figure()
    plt.scatter(weight_dogs, tail_dogs, label='Dogs', alpha=0.6)
    plt.scatter(weight_cats, tail_cats, label='Cats', alpha=0.6)
    plt.legend()
    plt.xlabel('Weight (kg)')
    plt.ylabel('Tail length (cm)')
    
    
def make_graph_2():
    
    global w, t
    
    np.random.seed(0)
    fig, ax = plt.subplots()
    
    weight_dogs = 0.45 * (np.random.gamma(7.5, 10, 50))
    weight_cats = 0.45 * (3 + np.random.gamma(7.5, 1, 50))
    tail_cats = np.random.normal(45, 1.5, 50)
    tail_dogs = weight_dogs + np.random.normal(10, 10, 50)
    
    ax.scatter(weight_dogs, tail_dogs, label='Dogs', alpha=0.6)
    ax.scatter(weight_cats, tail_cats, label='Cats', alpha=0.6)
    plt.legend()
    plt.xlabel('Weight (kg)')
    plt.ylabel('Tail length (cm)')
    
    w, t = 0, 0
    point,  = plt.plot([55], [22], marker='o', linewidth=0, color='#1f77b4', alpha=0.6)
    colors = ['#ff7f0e', '#1f77b4']
    
    data = np.zeros((100, 3))
    data[:50, 0] = weight_dogs
    data[:50, 1] = tail_dogs
    data[:50, 2] = 1
    data[50:, 0] = weight_cats
    data[50:, 1] = tail_cats
    data[50:, 2] = 0
    
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
    
    def update_weight(weight=22):
        global w, t
        
        w = weight
        point.set_xdata([weight])
        update()

    def update_tail(tail=55):
        global w, t
        
        t = tail
        point.set_ydata([tail])    
        update()

    interact(update_weight, weight=(0, 70, 0.01))
    interact(update_tail,   tail=(10, 70, 0.01))
    

def make_graph_3():
    
    global X1, X2, Y1, Y2
    
    fig, ax = plt.subplots()
    
    plt.xlabel('x')
    plt.ylabel('y')
    ax.set_ylim(0, 5)
    ax.set_xlim(0, 5)
    ax.set_yticks(np.arange(5))
    ax.set_xticks(np.arange(5))
    ax.grid(alpha=0.5)
    
    
    X1, X2, Y1, Y2 = 1.5, 1.5, 3.5, 3.5 
    
    points, = ax.plot([X1, X2], [Y1, Y2], marker='o', linewidth=0, color='#1f77b4')
    line, = ax.plot([X1, X2], [Y1, Y2], alpha=0.7)
    
    line_x, = ax.plot([X1, X2], [Y1, Y1], ls='--', color='k', alpha=0.5)
    line_y, = ax.plot([X2, X2], [Y1, Y2], ls='--', color='k', alpha=0.5)
    
    def update():
        global X1, X2, Y1, Y2
        
        points.set_xdata([X1, X2])
        line.set_xdata([X1, X2])
        line_x.set_xdata([X1, X2])
        line_y.set_xdata([min((Y1, X2), (Y2, X1), key=lambda x: x[0])[1]] * 2)

        points.set_ydata([Y1, Y2])
        line.set_ydata([Y1, Y2])
        line_x.set_ydata([min(Y1, Y2)] * 2)
        line_y.set_ydata([Y1, Y2])
        
        d = ((X2 - X1) ** 2 + (Y2 - Y1) ** 2) ** 0.5
        s = '({:.2f} - {:.2f})^2 + ({:.2f} - {:.2f})^2'.format(X2, X1, Y2, Y1)
        ax.set_title('$d = \sqrt{' + s + '}' + f'={d:.2f}' + '$')


    def update_x1(x1=1.5):
        global X1
        X1 = x1
        update()
        
    def update_x2(x2=3.5):
        global X2
        X2 = x2
        update()
        
    def update_y1(y1=1.5):
        global Y1
        Y1 = y1
        update()
        
    def update_y2(y2=3.5):
        global Y2
        Y2 = y2
        update()
                         
    interact(update_x1, x1=(0, 5, 0.001))
    interact(update_y1, y1=(0, 5, 0.001))
    interact(update_x2, x2=(0, 5, 0.001))
    interact(update_y2, y2=(0, 5, 0.001))
    
def test_exercise_1(f):
    
    inputs = np.random.normal(size=(10, 4))
    out = ((inputs[:, 0] - inputs[:, 2]) ** 2 + (inputs[:, 1] - inputs[:, 3]) ** 2 ) ** 0.5

    outt = [f(*inputs[i, :]) for i in range(10)]
    
    try:
    
        if np.allclose(out, outt):
            print('Congratulations! Your code passed all the tests :D')

        else:
            print("Your function is returning a number fine, but it looks like its producing the wrong output:'( Try taking another look")
            
    except:
        print("Unfortunately there is a problem with your function :'( Try taking another look. \n Things to try: \n1. Is your function returning anything? \n2. Have you indented your function properly? Make sure it looks similar to the example above \n3. Have you used brackets correctly? ")
        

def make_graph_4():
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    np.random.seed(0)

    weight_dogs = 0.45 * (np.random.gamma(7.5, 10, 50))
    weight_cats = 0.45 * (3 + np.random.gamma(7.5, 1, 50))
    tail_cats = np.random.normal(45, 1.5, 50)
    tail_dogs = weight_dogs + np.random.normal(10, 10, 50)
    paw_dogs = weight_dogs + np.random.normal(10, 10, 50)
    paw_cats = np.random.normal(20, 5, 50)

    ax.scatter(weight_dogs, tail_dogs, paw_dogs)
    ax.scatter(weight_cats, tail_cats, paw_cats )

    ax.set_xlabel('Weight (kg)')
    ax.set_ylabel('Tail length (cm)')
    ax.set_zlabel('Paw width (mm)')
    

def test_exercise_3(f):
    
    inputs = np.random.normal(size=(10, 6))
    out = ((inputs[:, 0] - inputs[:, 3]) ** 2 + (inputs[:, 1] - inputs[:, 4]) ** 2 + (inputs[:, 2] - inputs[:, 5]) ** 2) ** 0.5

    outt = [f(*inputs[i, :]) for i in range(10)]
    
    try:
    
        if np.allclose(out, outt):
            print('Congratulations! Your code passed all the tests :D')

        else:
            print("Your function is returning a number fine, but it looks like its producing the wrong output:'( Try taking another look")
            
    except:
        print("Unfortunately there is a problem with your function :'( Try taking another look. \n Things to try: \n1. Is your function returning anything? \n2. Have you indented your function properly? Make sure it looks similar to the example above \n3. Have you used brackets correctly? ")
        
        
def test_bonus_exercise(f):
    
    data = np.array([[ 0.55188725, 26.08753489, 37.13760502],
                     [64.54780232,  6.26461815, 28.41596254],
                     [ 1.70192398, 23.9827689 , 43.55617412],
                     [19.53475638, 14.68249648,  8.09922633],
                     [40.39981708, 48.66890041, 47.03699984],
                     [66.42027145,  0.18922497, 45.30376577],
                     [42.0274566 , 41.2117727 , 67.39392239],
                     [ 1.18101714, 48.75377015, 56.95750548],
                     [35.68650376, 23.37754087, 55.35881143],
                     [ 6.80700479, 30.94249464, 36.39666622]])
    
    correct = ['Cat', 'Dog', 'Cat', 'Cat', 'Dog', 'Dog', 'Dog', 'Cat', 'Dog', 'Cat']
    
    try:
        answer = [f(*data[i, :]) for i in range(10)]
        
        if all([ans == cor for ans, cor in zip(answer, correct)]):
            print('Congratulations! Your function is perfect!')
        else:
            print('Nearly there!! Try taking another look')
            
    except:
        print('It seems your function is a little broken! Try taking another look')
    

