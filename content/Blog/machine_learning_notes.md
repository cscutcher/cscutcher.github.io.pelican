Title: Notes on Machine Learning
Tags: machine-learning, notes
Status: draft

This page contains some notes written when taking the excellent 
[Coursera Machine Learning Course from Stanford](https://www.coursera.org/learn/machine-learning/)
.

I've almost certainly made some mistakes but I figured I'd write them here for
my convenience and publish them in case others find them useful.

[TOC]

Linear Regression
=================
** [See week 2](https://www.coursera.org/learn/machine-learning/home/week/2) ** 


$$
h_\theta(x) = \sum_{j=0}^n \theta_j x_j \\
h_\theta(x) = \theta^T x
$$

$$
J(\theta) = \frac{1}{2m} \left[ { \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)} ) ^ 2} \right]   \\
\theta_j := \theta_j - \alpha\frac{1}{m}\left[ \sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})x_j^{(i)}\right]  
$$

Logistic Regression
===================
** [See week 3](https://www.coursera.org/learn/machine-learning/home/week/3) ** 

* Linear regression won't work!
* Sigmoid function ensures convex cost graph
* $h_\theta(x)=P(y=1|x;0)$

$$
h_\theta(x) = g(\theta ^ Tx)\\
g(z) = \frac{1}{1+e^{-z}}\\
h_\theta(x) = \frac{1}{1+e^{-\theta^Tx}}
$$


Dealing with fitting with Regularization
========================================
** [See week 4](https://www.coursera.org/learn/machine-learning/home/week/4) ** 


Data fitting
------------

**Underfitting** : 'High bias' when learned hypothesis does not fit very well. 

**Overfitting**: 'High variance' when the learned hypothesis adheres too closely
to training data.

If we have too many **features** the learned hypothesis may fit training set
very well, but fail to generalise to new examples.

How to address overfitting
--------------------------
* Reduce number of features.
* Regularization;
    + Keep all features but reduce their magnitude.
    + Works well with many features.


Regularization to deal with overfitting
---------------------------------------
Works by optimizing down magnitude of $\theta$ in addition to the cost which is
already being .


Regularizing Linear Regression
------------------------------

$$
J(\theta) = \frac{1}{2m} \left[ \color{green} { \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)} ) ^ 2} + \color{red}{\leftthreetimes \sum_{i=1}^{N} \theta_j^2 } \right]
$$

$$
\theta_j := \theta_j - \alpha\left[\frac{1}{m} \sum_{i=1}^m(h_\theta(x^{(i)})-y^{(i)})x_j^{(i)}+\frac{\leftthreetimes}{m}\theta_j\right]
$$

or rewritten as

$$
\theta_j := \theta_j \left(1-\alpha \frac{\leftthreetimes}{m} \right) - \alpha \frac{1}{m} \sum_{i=2}^m \left(h_\theta ( x^{(i)} ) - y^{(i)} \right) x_j^{(i)}
$$

** Do not regularise $\theta_0$ **

Green is the original cost parameter. It's goal is to make the hypothesis fit
the training data.

Red is the regularization parameter. It's goal is to simplify the hypothesis by
reducing the magnitude of $\theta$.


Regularizing Linear Regression with Normal Equation
---------------------------------------------------
TODO: Notes on regularizing normal equation

Regularizing Logistic Regression
--------------------------------

$$
J(\theta) = \left[ -\frac{1}{m} \sum_{i=1}^{n} y^{(i)} \log(h_\theta(x^{(i)}) + (1-y^{(i)}) \log (1-h_\theta (x^{(i)}) \right] + \frac{\leftthreetimes}{2m} \sum_{j=1}^{m} \theta_j^2 
$$

$$
\text{grad} = \frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)}) x_j^{(i)} + \frac{\leftthreetimes}{m} \theta_j
$$


Effect of $\leftthreetimes$
-----------------------------

If $\leftthreetimes$ is **too high**  then we will see an underfit.

If $\leftthreetimes$ is **too low**  then we will see an overfit.

Neural Networks
===============
** [See week 4](https://www.coursera.org/learn/machine-learning/home/week/4)
and exercise 3 ** 

* Well suited to non-linear problems that would require many features.
* Feature complexity for scales at something like $O(n^2)$ or
  $O\left(\frac{n^2}{2}\right)$
* Popular in 1980-1990s, but also seen resurgence recently.
* State of the art for many applications.

Representation
--------------
Here's a couple of slides that are easier to just include rather than rewrite;

![Slide introducing non-vectorized NN representation]({filename}/images/machine_learning_coursera_nn_0.png)

![Slide introducing vectorized NN representation]({filename}/images/machine_learning_coursera_nn_1.png)

If network has $s_j$ units in layer $j$ and $s_{(j+1)}$ in layer $j+1$
then $\theta(j)$ will be dimensions;
$$
s_{(j+1)} \times (s_j + 1)
$$

Lingo
-----
* $x_0$ = bias unit
* Sigmoid/Logistic **Activation Function**
* $\theta$ == weights == parameters
* Layer 1 = Input Layer. Layer [-1] = Output Layer. Layer [others] = Hidden layer.
* $a_i^{(j)}$ is "activating of unit $i$ in layer $j$.
* $\theta{(j)}$ is matrix of weights controlling function mapping from layer
  $j$ to layer $j+1$.

Cost Function
-------------

$$
J(\theta)= \frac{1}{m}\sum^m_{i=1}\sum^K_{k=1}\left[ - y_k^{(i)}\log \left( \left( h_\theta ( x^{(i)} ) \right)k \right) - \left( 1 - y_k^{(i)} \right) \log \left( 1 - \left( h_\theta(x^{(i)}) \right)  k\right) \right] + \\
\frac{\leftthreetimes}{2m}\left[ \sum^{25}_{j=1}\sum^{400}_{k=1} \left( \theta_{j,k}^{(1)} \right)^2 + \sum^{10}_{j=1}\sum^{25}_{k=1} \left( \theta_{j,k}^{(2)} \right)^2 \right]
$$

** Note that $J(\theta)$ is non-convex and may converge on lcal minima **


Grad Function/Back Prop
-----------------------

$$
\text{sigmoid}(z)=g(z)=\frac{1}{1+e^{-z}}\\
g'(z)=\frac{d}{dz}g(z)=g(z)(1-g(z))
$$

1. Forward propagate to get activation values for all units.
2. Calculate $\delta$ for output unit: 
$$
\delta_k^{\text{end}} = (a_k^{(\text{end})} - y_k)
$$
3. For all other layers;
$$
\delta^{(l)} = (\theta^{(l)})^T\delta^{(l+1)}(a^{(l)})^T
$$
4. Accumulate the gradient with following formula.
$$
\triangle^{(l)} = \triangle^{(l)} + \delta^{(l+1)}(a^{(l)})^T
$$
Remove $\delta_0^{l}$.
5. Obtain the gradient for $j=0$:
$$
\frac{\partial}{\partial\theta_{ij}^{(l)}}J(\theta)=D_{ij}^{(l)}=\frac{1}{m}\triangle_{ij}^{(l)}
$$
for $j>=1$
$$
\frac{\partial}{\partial\theta_{ij}^{(l)}}J(\theta)=D_{ij}^{(l)}=\frac{1}{m}\triangle_{ij}^{(l)} + \frac{\leftthreetimes}{m}\theta_{ij}^{(l)}
$$

Initialising $\theta$
---------------------
** Don't initialise to all the same value as nn will get *stuck* **

Initialise each to random value between $\epsilon$ and $-\epsilon$.

Architecture
------------
When choosing architecture a reasonable initial step is to choose 3 layer design

* Input layer
* Hidden layer
* Output layer

If using more layers (say $n$) start with same units per layer.
More units per layer is usually *better*.

Gradient Checking
-----------------
Gradient checking can be used to check implementation.
It should not be used exhaustively as it's too expensive to calculate. 

$$
f_i(\theta) \approx \frac{J(\theta^{i+\epsilon}) - J(\theta^{i-\epsilon})}{2\epsilon}
$$

```octave
for i = 1:n
    thetaPlus = theta;
    thetaPlus(i) = thetaPlus(i) + EPSILON;
    thetaMinus = theta;
    thetaMinus(i) = thetaMinus(i) - EPSILON;
    gradApprox(i) = (J(thetaPlus) - J(thetaMinus)) / (2*EPSILON)
end;
```

$\text{gradApprox} \approx \text{DVec}$


Excercise 4 Results
-------------------

![Excercise 4 Output]({filename}/images/machine_learning_ex4_output.png)

* 50 iterations. 96.14% accuracy.
* 250 iterations. 99.36% accuracy.
* 500 iterations. 99.4% accuracy.

On actual (biological) neurons
------------------------------
* Dendrite is 'input'
* Axon is 'output'
