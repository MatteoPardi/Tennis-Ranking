# Bayesian Tennis Ranking

Let's say we have a database of tennis matches like the following:


```python
from tennis_tools import TennisUniverse

tu = TennisUniverse('data.csv')
tu.df.reset_index()[['players A', 'players B', 'score', 'tournament']]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>players A</th>
      <th>players B</th>
      <th>score</th>
      <th>tournament</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Donatello Luciani</td>
      <td>Pellegrino Giovine</td>
      <td>6-4 6-1</td>
      <td>AICS 2023</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Lorenzo Bellomo, Matteo Pardi</td>
      <td>Marcello Cibin, Pierluigi Pacomio</td>
      <td>6-1 6-1</td>
      <td>AICS 2023</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Pardi Marco</td>
      <td>Lucio Conte</td>
      <td>6-1 7-6</td>
      <td>AICS 2023</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Calogero Battelli</td>
      <td>Uberto Oliboni</td>
      <td>6-0 6-4</td>
      <td>AICS 2023</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Giuseppe Cavalcanti, Gioacchino Flaiano</td>
      <td>Federico Gatto, Delfino Mozart</td>
      <td>6-1 6-0</td>
      <td>AICS 2023</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>379</th>
      <td>Fulvio Zoppetti</td>
      <td>Gianni Guarana</td>
      <td>5-7 2-6</td>
      <td>Mr. Dodo 22 - Fase Eliminatoria</td>
    </tr>
    <tr>
      <th>380</th>
      <td>Atenulf Solimena, Adriano Spinelli</td>
      <td>Giacinto Orengo, Manuel Cannizzaro</td>
      <td>5-7 3-6</td>
      <td>Mr. Dodo 22 - Fase Eliminatoria</td>
    </tr>
    <tr>
      <th>381</th>
      <td>Gabriele Fantoni</td>
      <td>Ennio Rizzoli</td>
      <td>3-6 7-6 7-10</td>
      <td>Mr. Dodo 22 - Fase Eliminatoria</td>
    </tr>
    <tr>
      <th>382</th>
      <td>Manuel Cannizzaro</td>
      <td>Pasqual Dovara</td>
      <td>6-3 7-6</td>
      <td>Mr. Dodo 22 - Fase Eliminatoria</td>
    </tr>
    <tr>
      <th>383</th>
      <td>Donato Cattaneo, Sebastiano Alfieri</td>
      <td>Ubaldo Ramazzotti, Gioffre Farina</td>
      <td>6-3 6-3</td>
      <td>Mr. Dodo 22 - Fase Eliminatoria</td>
    </tr>
  </tbody>
</table>
</div>



We would like to get a players' ranking of the form




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>ability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Giuseppe Cavalcanti</td>
      <td>108.079536</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Gianluigi Caccianemico</td>
      <td>105.692780</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cirillo Pisaroni</td>
      <td>105.672729</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ottone Basadonna</td>
      <td>105.509888</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Dionigi Vecellio</td>
      <td>105.113510</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>200</th>
      <td>Nanni Lucchesi</td>
      <td>93.622917</td>
    </tr>
    <tr>
      <th>201</th>
      <td>Marcello Cibin</td>
      <td>92.758682</td>
    </tr>
    <tr>
      <th>202</th>
      <td>Ranieri Trapani</td>
      <td>92.602478</td>
    </tr>
    <tr>
      <th>203</th>
      <td>Gionata Gulotta</td>
      <td>91.815338</td>
    </tr>
    <tr>
      <th>204</th>
      <td>Valerio Aporti</td>
      <td>91.770103</td>
    </tr>
  </tbody>
</table>
</div>



Typical ranking methods are based on the 'you update when you play' rule:
- each time a player plays a match its ability changes
- the ability doesn't change if the player doesn't play (or decreases as player's inactivity increases)
- if a player wins its ability grows
- if a player lose its ability decreases

There are several reasons not to trust this type of ranking methods. They can be easly understood by some example situations:
1. There are five players: A, B, C, D, E. Let's say A wins against B, and then B wins against C, D and E. Since B won 3 matches and A just one, B will have a greater ability respect to A. But this is not what we would like to have, since A won against B... A should be considered stronger than B.
2. Today A and B have the same ability, since they got similar results in their matches, played more or less with the same people. For a short period, A stops to play, while B continues. In this short period, B loses all matches he plays. This fact reveals that the ability of B was overrated: probably B had been lucky up to now in playing only against weak people. Thus, the ability of B decreases... but the ability of A remains the same. This is not what we would like to have, since we know that A and B should have similar abilities.

Here we present a new method not based on the 'you update when you play' rule, but on rigorous bayesian statistics built on a simple mathematical model for tennis matches.

### The Model

The model is very simple. Each player $j = 1, \dots, M$ has an ability $a_j \in \mathbb{R}$. A tennis match (let's say: player $A$ vs player $B$) is a sequence of independent points. Each point is described by a Bernoulli distribution with probability $\psi$, where $\psi$ is the probability that $A$ wins the point. $\psi$ depends from the players' abilities according to the following logistic-like formula:
$$
\psi = \frac{1}{2} + \frac{1}{\pi} \arctan \left( \frac{a_A - a_B}{10} \right) \ .
$$

This completely defines the likelihood of a match score $s$
$$
p(s|a_A, a_B)
$$

which can be derived analytically without particular difficulties (given the scoring system of the tournament we are interested to).

Treating the database as a set of independent matches, with scores $s_i$ where $i = 1, \dots, N$, we can compute the (log)likelihood of the data
$$
\log p(s_1, \dots, s_N | a_1, \dots, a_M) = \sum_{i=1}^{N} \log p (s_i | a_A^{(i)}, a_B^{(i)})
$$

To get the abilities from the database, we could find the maximum likelihood estimator of the abilities. Instead of doing this, it is a good practice to introduce a (log)-prior bayesian term to regularize the optimization. As instance, assuming a Gaussian distribution with mean 0 (useful also to break the translational symmetry of the model during the optimization) and std 5 (intuitively reasonable by looking at the $\psi$-formula) we get as loss function to minimize:
$$
\mathcal{L}(a_1, \dots, a_M) = -\log p(s_1, \dots, s_N | a_1, \dots, a_M) + \frac{1}{50} \sum_{j=1}^{M} {a_j}^2
$$

Thus, a first proposal to get the desidered ranking could be
$$
\mathbf{\hat{a}} = \mathrm{argmin} \, \mathcal{L}(\mathbf{a})
$$

but conventionally, to break the translational symmetry of the model in an useful way, we translate $\mathbf{\hat{a}}$ so that its median is 100: the definitive ranking $\mathbf{a}$ is then
$$
\mathbf{a} = \mathbf{\hat{a}} - \mathrm{median} (\mathbf{\hat{a}}) + 100
$$