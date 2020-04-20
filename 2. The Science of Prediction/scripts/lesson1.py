from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets.widgets import interact
from math import erf

def make_graph_1():
    
    c = Counter()

    fig, ax = plt.subplots()

    bars = ax.bar(range(4), np.zeros(4), alpha=0.6)
    ax.set_xticks(range(4))
    suits = ['♠️', '♣️', '♦️', '♥️']
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    ax.set_xticklabels(suits)
    ax.set_ylim(0, 1.1)
    
    plt.xlabel('Suit')
    plt.ylabel('Number selected')

    button = widgets.Button(description="Select a card")
    output = widgets.Output()

    display(button, output)

    def on_button_clicked1(b):
        n = np.random.randint(0, 4)
        c[n+1] += 1
        with output:
            bars[n].set_height(bars[n].get_height() + 1)
        ax.set_title(np.random.choice(cards)+suits[n])

        ax.set_ylim(0, 1.1 * max(c.values()))

    button.on_click(on_button_clicked1)
    
    
def make_graph_2():
    
    global fill, p, text
    
    fig, ax = plt.subplots()

    plt.plot([0,0,2, 2], [0, 0.5, 0.5, 0])
    ax.set_ylim(0, 0.55)

    a, = ax.plot([0.2, 0.2], [0, 0.5], ls='--', color='k', alpha=0.5)
    b, = ax.plot([0.5, 0.5], [0, 0.5], ls='--', color='k', alpha=0.5)

    fill = ax.fill_between([0.2, 0.5], [0, 0], [0.5, 0.5], alpha=0.5, color='#1f77b4')

    p = [0.2, 1.5]
    
    ax.set_title(f'Probability of being between {0.2:.2f} and {0.5:.2f} is {0.65}')
    text = ax.text((p[1] + p[0])/2, 0.25, f'Area = {0.65}', horizontalalignment='center')


    def update_a(A=0.2):
        global p, fill, text
        
        a.set_xdata([A, A])
        p[0] = A
        fig.canvas.draw_idle()
        fill.remove()
        fill = ax.fill_between([A, p[1]], [0, 0], [0.5, 0.5], alpha=0.5, color='#1f77b4')
        ax.set_title(f'Probability of being between {A:.2f} and {p[1]:.2f} is {abs(A - p[1])/2:.2f}')
        text.set_x((p[1] + p[0])/2)
        text.set_text(f'Area = {abs(p[0]- p[1])/2:.2f}')

    def update_b(B=1.5):
        global p, fill, text
        
        b.set_xdata([B, B])
        p[1] = B
        fig.canvas.draw_idle()
        fill.remove()
        fill = ax.fill_between([p[0], B], [0, 0], [0.5, 0.5], alpha=0.5, color='#1f77b4')
        ax.set_title(f'Probability of being between {p[0]:.2f} and {B:.2f} is {abs(p[1] - p[0])/2:.2f}')
        text.set_x((p[1] + p[0])/2)
        text.set_text(f'Area = {abs(p[0] - p[1])/2:.2f}')

    plt.ylabel('Probability Density')
    plt.xlabel('$x$')

    interact(update_a, A=(0, 2, 0.001))
    interact(update_b, B=(0, 2, 0.001))
    
    
def exercise_2_test(f):
    
    test_inputs = [(0, 2), (0, 1), (1, 2), (0.2, 1.8), (0.5, 0.7), (0, 0)]
    correct_answers = [1, 0.5, 0.5, 0.8, 0.1, 0]
    
    if f(0, 2) is None:
        return 'Your function is not returing anything! Make sure you use the keyword "return" to output the probability you have calculated'

    if all([np.isclose(f(a, b),  ans) for (a, b), ans in zip(test_inputs, correct_answers)]):
        return 'Congratulations! Your function passed all the tests!'
    else:
        return 'Your function is producing the wrong output for one or more of the tests. Try taking another look'
        


def make_graph_3():
    
    global fill, p, text
    
    fig, ax = plt.subplots()
    
    mu = 170
    sig = 6.5
    x = np.linspace(mu - 4.5* sig, mu + 4.5 * sig, 1001)
    
    def f(x):
        return (sig * (2 * np.pi) ** 0.5) ** -1 * np.exp(- (x - mu) ** 2 / (2 * sig ** 2))
    
    def F(x):
        return 0.5 * (1 + erf((x - mu) / (sig * 2 ** 0.5)))
    
    def P(a, b):
        return abs(F(b) - F(a))
    
    y = f(x)
    
    plt.plot(x, y)
    ax.set_ylim(0, 0.07)
    
    a0 = 160
    b0 = 170

    a, = ax.plot([a0, a0], [0, f(a0)], ls='--', color='k', alpha=0.5)
    b, = ax.plot([b0, b0], [0, f(b0)], ls='--', color='k', alpha=0.5)

    fill = ax.fill_between(np.linspace(a0, b0, 250), np.zeros(250), f(np.linspace(a0, b0, 250)), alpha=0.5, color='#1f77b4')

    p = [a0, b0]
    
    ax.set_title(f'Probability of having a height between {a0:.0f}cm and {b0:.0f}cm is {P(a0, b0):.2f}')
    text = ax.text((p[1] + p[0])/2, max(f(p[1]), f(p[0])) / 3, f'Area = {P(a0, b0):.2f}', horizontalalignment='center')


    def update_a(height1=160):
        global p, fill, text
        
        a.set_xdata([height1, height1])
        a.set_ydata([0, f(height1)])
        p[0] = height1
        fig.canvas.draw_idle()
        fill.remove()
        xax = np.linspace(p[0], p[1], 250)
        fax = f(xax)
        fill = ax.fill_between(xax, np.zeros(250), fax, alpha=0.5, color='#1f77b4')
        ax.set_title(f'Probability of having a height between {p[0]:.0f}cm and {p[1]:.0f}cm is {P(p[0], p[1]):.2f}')
        text.set_x((p[1] + p[0])/2)
        text.set_y(fax.max() / 3)
        text.set_text(f'Area = {P(p[0], p[1]):.2f}')

    def update_b(height2=170):
        global p, fill, text
        
        b.set_xdata([height2, height2])
        b.set_ydata([0, f(height2)])
        p[1] = height2
        fig.canvas.draw_idle()
        fill.remove()
        xax = np.linspace(p[0], p[1], 250)
        fax = f(xax)
        fill = ax.fill_between(xax, np.zeros(250), fax, alpha=0.5, color='#1f77b4')
        ax.set_title(f'Probability of having a height between {p[0]:.0f}cm and {p[1]:.0f}cm is {P(p[0], p[1]):.2f}')
        text.set_x((p[1] + p[0])/2)
        text.set_y(fax.max() / 3)
        text.set_text(f'Area = {P(p[0], p[1]):.2f}')
        
    plt.ylabel('Probability Density')
    plt.xlabel('Height, cm')

    interact(update_a, height1=(140, 200, 1))
    interact(update_b, height2=(140, 200, 1))
    
    
def make_graph_4():
    global fill, p, text
    
    fig, ax = plt.subplots()
    
    lamda = np.log(2) / 5700
    x = np.linspace(0, 40000, 1001)
    
    def f(x):
        if isinstance(x, np.ndarray):
            return lamda * np.exp(- lamda * x[x >= 0])
        else:
            if x > 0:
                return lamda * np.exp(- lamda * x)
            else:
                return 0
    
    def F(x):
        if isinstance(x, np.ndarray):
            return 1 -  np.exp(- lamda * x[x >= 0])
        else:
            if x > 0:
                return 1 - np.exp(- lamda * x)
            else:
                return 0
            
    def P(a, b):
        return abs(F(b) - F(a))
    
    y = f(x)
    
    plt.plot(x, y)
    ax.set_ylim(0, 0.00013)
    
    a0 = 5000
    b0 = 10000

    a, = ax.plot([a0, a0], [0, f(a0)], ls='--', color='k', alpha=0.5)
    b, = ax.plot([b0, b0], [0, f(b0)], ls='--', color='k', alpha=0.5)

    fill = ax.fill_between(np.linspace(a0, b0, 250), np.zeros(250), f(np.linspace(a0, b0, 250)), alpha=0.5, color='#1f77b4')

    p = [a0, b0]
    
    ax.set_title(f'Probability of decay between {a0:.0f} and {b0:.0f}y is {P(a0, b0):.2f}')
    text = ax.text((p[1] + p[0])/2, max(f(p[1]), f(p[0])) / 3, f'Area = {P(a0, b0):.2f}', horizontalalignment='center')

    def update_a(t1=5000):
        global p, fill, text
        
        a.set_xdata([t1, t1])
        a.set_ydata([0, f(t1)])
        p[0] = t1
        fig.canvas.draw_idle()
        fill.remove()
        xax = np.linspace(p[0], p[1], 250)
        fax = f(xax)
        fill = ax.fill_between(xax, np.zeros(250), fax, alpha=0.5, color='#1f77b4')
        ax.set_title(f'Probability of decay between {p[0]:.0f} and {p[1]:.0f}y is {P(p[0], p[1]):.2f}')
        text.set_x((p[1] + p[0])/2)
        text.set_y(fax.max() / 3)
        text.set_text(f'Area = {P(p[0], p[1]):.2f}')

    def update_b(t2=9000):
        global p, fill, text
        
        b.set_xdata([t2, t2])
        b.set_ydata([0, f(t2)])
        p[1] = t2
        fig.canvas.draw_idle()
        fill.remove()
        xax = np.linspace(p[0], p[1], 250)
        fax = f(xax)
        fill = ax.fill_between(xax, np.zeros(250), fax, alpha=0.5, color='#1f77b4')
        ax.set_title(f'Probability of decay between {p[0]:.0f} and {p[1]:.0f}y is {P(p[0], p[1]):.2f}')
        text.set_x((p[1] + p[0])/2)
        text.set_y(fax.max() / 3)
        text.set_text(f'Area = {P(p[0], p[1]):.2f}')
        
    plt.ylabel('Probability Density')
    plt.xlabel('Time, years')
    plt.tight_layout()

    interact(update_a, t1=(0, 40000, 100))
    interact(update_b, t2=(0, 40000, 100))            