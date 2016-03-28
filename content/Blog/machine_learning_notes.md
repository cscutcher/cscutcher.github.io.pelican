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
