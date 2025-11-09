---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
language_info:
  name: python
  pygments_lexer: ipython3
  nbconvert_exporter: python
---

# n-body problem

+++

pour faire cette activité sur votre ordi localement, {download}`commencez par télécharger le zip<ARTEFACTS-n-body.zip>`

dans ce TP on vous invite à écrire un simulateur de la trajectoire de n corps qui interagissent entre eux au travers de leurs masses, pour produire des sorties de ce genre

```{image} media/init3-1.png
:align: center
:width: 600px
```

+++

on suppose:

- on se place dans un monde en 2 dimensions
- on fixe au départ le nombre de corps N
- chacun est décrit par une masse constante
- et au début du monde chacun possède une position et une vitesse

```{admonition} la 3D
en option on vous proposera, une fois votre code fonctionnel en 2D, de passer à la 3D  
ça peut valoir le coup d'anticiper ça dès le premier jet, si vous vous sentez de le faire comme ça
```

+++

## imports

on pourra utiliser le mode `ipympl` de `matplotlib`

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt

%matplotlib ipympl
```

## initialisation aléatoire

en fixant arbitrairement des limites dans l'espace des positions, des vitesses et des masses, la fonction `init_problem()` tire au hasard une configuration de départ pour la simulation

```{code-cell} ipython3
# les bornes pour le tirage au sort initial
mass_max = 3.
    
x_min, x_max = -10., 10.
y_min, y_max = -10., 10.

speed_max = 1.
```

```python

def init_problem(N):
    masses = np.random.random(N) * mass_max
    positions = np.random.random((2, N))
    
    positions[0] = positions[0] * (x_max - x_min) + x_min
    positions[1] = positions[1] * (y_max - y_min) + y_min

    speeds = np.random.random((2, N)) * speed_max

    return masses, positions, speeds

```

```{code-cell} ipython3
:tags: [level_intermediate]

# pour tester

# normalement vous devez pouvoir faire ceci

masses, positions, speeds = init_problem(10)

# et ceci devrait afficher OK
try:
    masses.shape == (10,) and positions.shape == speeds.shape == (2, 10)
    print("OK")
except:
    print("KO")
```

## initialisation reproductible

par commodité on vous donne la fonction suivante qui crée 3 objets:

- le premier - pensez au soleil - de masse 3, an centre de la figure, de vitesse nulle
- et deux objets de masse 1, disposés symétriquement autour du soleil  
  - position initiale (5, 1) et vitesse initiale (-1, 0)
  - symétrique en     (-5, -1) et vitesse initiale (1, 0)

```{code-cell} ipython3
# for your convenience

def init3():
    # first element is sun-like: heavy, at the center, and no speed
    masses = np.array([3, 1, 1], dtype=float)
    positions = np.array([
        [0, 5, -5], 
        [0, 1, -1]], dtype=float)
        [0, -1, 1], 
        [0, 0, 0]], dtype=float)
    return masses, positions, speeds
```

## les forces

à présent, on va écrire une fonction qui va calculer les influences de toutes les particules entre elles, suivant la loi de Newton


$$
\vec{F}_i = \sum_{\substack{j=1 \\ j \neq i}}^N 
   G \, m_i m_j \, \frac{\vec{r}_j - \vec{r}_i}{\lvert \vec{r}_j - \vec{r}_i \rvert^3}
$$

pour cela on se propose d'écrire la fonction suivante

```python

def forces(masses, positions, G=1.0):

    #On a Fi = sum sur j != 1 de G mi mj (rj -ri) / |rj-ri|^3
    N = len(masses)
    x = positions[0] - (np.transpose(np.atleast_2d(positions[0])))
    y = positions[1] - (np.transpose(np.atleast_2d(positions[1])))

    #Je prépare le calcul de F. Je calcule la norme des différences des vecteurs 2 à 2, et je mets 1 lorsque je suis sur la diagonale pour éviter la division par 0
    #Ça n'affecte pas le calcul car ce terme est multiplié par zéro après.
    norme = (x ** 2 + y ** 2) + np.eye(N, N)
    norme = norme ** (3/2)
    facteur = G * masses * np.transpose(np.atleast_2d(masses))
    
    forces = np.empty((2, N))
    forces[0] = np.sum(x * facteur / norme, axis = 1)
    forces[1] = np.sum(y * facteur / norme, axis = 1)

    return forces

```

```{code-cell} ipython3
:tags: [level_intermediate]

# pour tester, voici les valeurs attendues avec la config prédéfinie

masses, positions, speeds = init3()

f = forces(masses, positions)

# should be true
# np.all(np.isclose(f, np.array([
#     [ 0.        , -0.12257258,  0.12257258],
#     [ 0.        , -0.02451452,  0.02451452]])))
```

## le simulateur

à présent il nous reste à utiliser cette brique de base pour "faire avancer" le modèle depuis son état initial et sur un nombre fixe d'itérations

cela pourrait se passer dans une fonction qui ressemblerait à ceci

```python

def simulate(masses, positions, speeds, dt=0.1, nb_steps=100, G=1.0):
    #On a mdv = Fdt et dr = dv dt
    pos = np.empty((nb_steps, 2, len(masses)))
    speed = np.empty((nb_steps, 2, len(masses)))
    pos[0], speed[0] = positions, speeds
    
    for i in range(nb_steps-1):
        force = forces(masses, pos[i], G)
        pos[i+1] = pos[i] + speed[i]*dt
        speed[i+1] = speed[i] + dt * force / masses
    
    return pos
```

```{code-cell} ipython3
:tags: [level_intermediate]

# pour tester

SMALL_STEPS = 4

s = simulate(masses, positions, speeds, nb_steps=SMALL_STEPS)

try:
    if s.shape == (SMALL_STEPS, 2, 3):
        print("shape OK")
except Exception as exc:
    print(f"OOPS {type(exc)} {exc}")
```

```{code-cell} ipython3
:tags: [level_intermediate]

# pour tester: should be true

# first step
# positions1 = s[1]

# np.all(np.isclose(positions1, np.array([
#     [ 0.        ,  4.89877427, -4.89877427],
#     [ 0.        ,  0.99975485, -0.99975485]
# ])))
```

## dessiner

ne reste plus qu'à dessiner; quelques indices potentiels:

- 1. chaque corps a une couleur; l'appelant peut vous passer un jeu de couleurs, sinon en tirer un au hasard
- 2.a pour l'épaisseur de chaque point, on peut imaginer utiliser la masse de l'objet  
  2.b ou peut-être aussi, à tester, la vitesse de l'objet (plus c'est lent et plus on l'affiche en gros ?)

```{admonition} masses et vitesses ?
j'ai choisi de repasser à `draw()` le tableau des masses à cause de 2.a;  
si j'avais voulu implémenter 2.b il faudrait tripoter un peu plus nos interfaces - car en l'état on n'a pas accès aux vitesses pendant la simulation - mais n'hésitez pas à le faire si nécessaire..
```

```python

def draw(simulation, masses, colors=None, scale=10.):
    plt.figure(figsize=(10, 6))

    cond = (colors != None and len(colors)>=len(masses))
    for i in range(len(masses)):
        plt.scatter(simulation[:, 0, i], simulation[:, 1, i], color=(colors[i] if cond else None), s=scale * masses[i])
        plt.plot(simulation[:, 0, i], simulation[:, 1, i], color=(colors[i] if cond else None), lw=0.5)

    plt.show()
    
```

## un jeu de couleurs

```{code-cell} ipython3
# for convenience

colors3 = np.array([
    [32, 32, 32],
    (228, 90, 146),
    (111, 0, 255),
]) / 255
```

## on assemble le tout

pour commencer et tester, on se met dans l'état initial reproductible

```{code-cell} ipython3
:tags: [level_intermediate]

# décommentez ceci pour tester votre code

# masses, positions, speeds = init3()
# draw(simulate(masses, positions, speeds), masses, colors3)
```

et avec ces données vous devriez obtenir plus ou moins une sortie de ce genre  
mais [voyez aussi la discussion ci-dessous sur les diverses stratégies possibles](label-n-body-strategies)
```{image} media/init3-1.png
```

+++

`````{grid} 2 2 2 2 
````{card}
après vous avez le droit de vous enhardir avec des scénarii plus compliqués
par exemple avec ce code

```python
m5, p5, s5 = init_problem(5)
sim5 = simulate(m5, p5, s5, nb_steps=1000)
draw(sim5, m5, scale=3);
plt.savefig("random5.png")
```
````
````{card}
j'ai pu obtenir ceci
```{image} media/random5.png
```
````
`````

+++

***
***
***

+++

## partie optionnelle

+++

### option 1: la 3D

```python
#Partie 3D. On peut envisager de simplement ajouter une dimension à la main
# sur tout le code, sans le modifier de manière à travailler en dimension d, ce que l'on pourrait toute fois faire avec des tableaux mais n'aurait pas d'intérêt car d ne dépassera jamais 3
#Ceci donnerait simplement : 

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

mass_max = 3.
    
x_min, x_max = -10., 10.
y_min, y_max = -10., 10.
z_min, z_max = -10., 10.

speed_max = 1.

def init_problem(N):
    masses = np.random.random(N) * mass_max
    positions = np.random.random((3, N))
    
    positions[0] = positions[0] * (x_max - x_min) + x_min
    positions[1] = positions[1] * (y_max - y_min) + y_min
    positions[2] = positions[2] * (z_max - z_min) + z_min

    speeds = np.random.random((3, N)) * speed_max

    return masses, positions, speeds


def forces(masses, positions, G=1.0):
    N = len(masses)
    x = positions[0] - (np.transpose(np.atleast_2d(positions[0])))
    y = positions[1] - (np.transpose(np.atleast_2d(positions[1])))
    z = positions[2] - (np.transpose(np.atleast_2d(positions[2])))

    norme = (x ** 2 + y ** 2 + z ** 2) + np.eye(N, N)
    norme = norme ** (3/2)
    facteur = G * masses * np.transpose(np.atleast_2d(masses))
    
    forces = np.empty((3, N))
    forces[0] = np.sum(x * facteur / norme, axis = 1)
    forces[1] = np.sum(y * facteur / norme, axis = 1)
    forces[2] = np.sum(z * facteur / norme, axis = 1)

    return forces

def simulate(masses, positions, speeds, dt=0.1, nb_steps=100, G=1.0):
    pos = np.empty((nb_steps, 3, len(masses)))
    speed = np.empty((nb_steps, 3, len(masses)))
    pos[0], speed[0] = positions, speeds
    
    for i in range(nb_steps-1):
        force = forces(masses, pos[i], G)
        pos[i+1] = pos[i] + speed[i]*dt
        speed[i+1] = speed[i] + dt * force / masses
    
    return pos

def draw(simulation, masses, colors=None, scale=10.):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    nb_steps, _, N = simulation.shape

    cond = (colors != None and len(colors) >= N)

    for i in range(N):
        x = simulation[:, 0, i]
        y = simulation[:, 1, i]
        z = simulation[:, 2, i]

        ax.scatter(x, y, z, color=(colors[i] if cond else None), s=(masses[i] / np.max(masses) * scale * 5) + 5)

        ax.plot(x, y, z, color=(colors[i] if cond else None), lw=0.7)


    ax.set_xlim([np.min(simulation[:, 0, :]), np.max(simulation[:, 0, :])])
    ax.set_ylim([np.min(simulation[:, 1, :]), np.max(simulation[:, 1, :])])
    ax.set_zlim([np.min(simulation[:, 2, :]), np.max(simulation[:, 2, :])])

    plt.show()
```    

+++

### option 2: un rendu plus interactif

le rendu sous forme de multiples scatter plots donne une idée du résultat mais c'est très améliorable  
voyez un peu si vous arrivez à produire un outil un peu plus convivial pour explorer les résultats de manière interactive; avec genre

- une animation qui affiche les points au fur et à mesure du temps
- qu'on peut controler un peu comme une vidéo avec pause / backward / forward
- l'option de laisser la trace du passé
- et si vous avez un code 3d, la possibilité de changer le point de vue de la caméra sur le monde
- etc etc...

voici une possibilité avec matplotlib; mais cela dit ne vous sentez pas obligé de rester dans Jupyter Lab ou matplotlib, il y a plein de technos rigolotes qui savent se décliner sur le web, vous avez l'embarras du choix...

```{code-cell} ipython3
:tags: [prune-remove-input, remove-input]

# prune-remove-input

# credit: Damien Corral
# with good old matplotlib FuncAnimation

from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def animate(simulation, masses, colors=None, scale=5., interval=50):
    nb_steps, _, N = simulation.shape
    colors = (colors if colors is not None
              else np.random.uniform(0.3, 1., size=(N, 3)))

    fig, ax = plt.subplots()
    ax.set_title(f"we have {N} bodies over {nb_steps} steps")

    ax.set_xlim(simulation[:, 0].min() - 1, simulation[:, 0].max() + 1)
    ax.set_ylim(simulation[:, 1].min() - 1, simulation[:, 1].max() + 1)

    scat = ax.scatter(np.zeros(N), np.zeros(N), c=colors, s=(masses*scale)**2)

    def init():
        scat.set_offsets(np.zeros((nb_steps, N)))
        return scat

    def update(step):
        x, y = simulation[step]
        scat.set_offsets(np.c_[x, y])
        return scat

    animation = FuncAnimation(
        fig, update, frames=nb_steps,
        init_func=init, blit=True, interval=interval
    )
    plt.close()
    return animation

def animate_from_file(filename):
    simulation = np.loadtxt(filename).reshape((100, 2, 3))
    animation = animate(simulation, masses, colors=colors3)
    return HTML(animation.to_jshtml())

animate_from_file("data/init3-simu-1.txt")
```

(label-n-body-strategies)=
## plusieurs stratégies

Pour les curieux, vous avez sans doute observé qu'il y a plusieurs façons possibles d'écrire la fonction `simulate()`

dans ce qui suit, on note l'accélération $a$, la vitesse $s$ et la position $p$

````{admonition} Approche 1
:class: note
dans l'implémentation qui a servi à calculer l'illustration ci-dessus, on a écrit principalement ceci:
- on calcule l'accélération
- ce qui permet d'extrapoler les vitesses  
  $s = s + a.dt$
- et ensuite d'extrapoler les positions  
  $p = p + s.dt$
```{admonition} 1bis
:class: tip
une variante consiste à intervertir les deux, en arguant du fait que la vitesse à l'instant $t$ agit sur la position à l'instant $t$
- on extrapole d'abord les positions
- puis seulement on calcule l'accélération
- enfin on extrapole les vitesses
```
````
````{admonition} Approche 2
:class: tip
dans cette approche plus fine, on utiliserait deux versions de l'accélération (l'instant présent et l'instant suivant), et un dévelopmment du second ordre, ce qui conduirait à
- calculer la position comme $p = p + s.dt + \frac{a}{2}.dt^2$
- calculer les accélérations $a_+$ sur la base de cette nouvelle position
- estimer l'accélération sur l'intervalle comme la demie-somme entre les deux accélérations
  $a_m = (a+a_+)/2$
- mettre à jour les vitesses
  $s = s + a_m.dt$
- ranger $a_+$ dans $a$ pour le prochain instant
````

+++

Bref, vous voyez qu'il y a énormément de liberté sur la façon de s'y prendre  
Ce qui peut expliquer pourquoi vous n'obtenez pas la même chose que les illustrations avec pourtant les mêmes données initiales

D'autant que, c'est bien connu, ce problème des n-corps est l'exemple le plus célèbre de problème instable, et donc la moindre divergence entre deux méthodes de calcul peut entrainer de très sérieux écarts sur les résultats obtenus

+++

Voici d'ailleurs les résultats obtenus avec ces deux approches alternatives, et vous pouvez constater qu'effectivement les résultats sont tous très différents !

+++

### approche 1bis

+++

````{grid} 2 2 2 2 
```{image} media/init3-1bis.png
```
```{code-cell} python
:tags: [remove-input]
animate_from_file("data/init3-simu-1bis.txt")
```
````

+++

### approche 2

+++

````{grid} 2 2 2 2 
```{image} media/init3-2.png
```
```{code-cell} python
:tags: [remove-input]
animate_from_file("data/init3-simu-2.txt")
```
````
