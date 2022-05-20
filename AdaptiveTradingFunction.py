# -*- coding: utf-8 -*-
"""
Created on Thu May 19 21:35:54 2022

Author: Giddy


AdaptiveTradingFunction.py

functions for modeling the adaptive trading function for the Adaptive Market 
Maker Chainlin Hackathon 2022 project.

"""

import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt


def calculate_k(q, x=100, y=100):
    """
    Calculate the invariant of a pool with reserves of x and y of tokens X and Y,
    respectively, with a q-value as specified. 
    
    Here, x**q + y**q = k**q

    Parameters
    ----------
    q : float, Decimal
        parameter determining the curvature of the trading function, and 
        therefore the form of the invariant function.
        
    x : float, Decimal, optional
        Amount of reserves of token X in the liquidity pool. The default is 100.
    y : float, Decimal, optional
        Amount of reserves of token Y in the liquidity pool. The default is 100.

    Returns
    -------
    k : Decimal
        the constant invariant, given the input parameters for the pool.

    """

    q = Decimal(q)
    x = Decimal(x)
    y = Decimal(y)
    if np.isclose(float(q),0):
        k = x*y
    else:
        k = (x**q + y**q)**(1/q)
    return k


def calculate_y_vec(xvec,q, k):
    """
    Given a set of x values (token X reserves in pool), along with a q value 
    and an invariant k values, this function calculates the corresponding y 
    coordinates (token Y reserves) on the particular trading curve.

    Parameters
    ----------
    xvec : list<float,Decimal>
        x-coordinate values.
    q : float, Decimal
        q parameter for determining the invariant function and form of trading
        curve.
    k : float, Decimal
        invariant for the trading function..

    Returns
    -------
    yvec : TYPE
        DESCRIPTION.

    """
    q = Decimal(q)
    k = Decimal(k)
    xvec = [Decimal(x) for x in xvec]
    yvec = []
    for x in xvec:
        try:
            if np.isclose(float(q),0):
                yvec.append(k / x)
            else:
                yvec.append((k**q - x**q)**(Decimal(1)/q))
        except:
            yvec.append(np.nan)
    return yvec


def plotFeasibleTradingCurves(xfraction = 0.5, yfraction = 0.5):
    """
    Plot the various bonding curves / trading curves for the various market 
    makers with different q values.

    Returns
    -------
    None.

    """
    xmax = 10000
    x = np.linspace(0.01, xmax, 100)
    qvals = np.arange(-0.8,0.8+0.2,0.2)
    plt.figure()
    for q in qvals:
        k = calculate_k(q, xfraction * xmax,yfraction * xmax)
        y = calculate_y_vec(x, q, k)
        if np.isclose(q,0):
            plt.plot(x,y,'k--',label=f"q={q:3.1f} : xy=const.")
        else:
            plt.plot(x,y,label=f"q={q:3.1f}")

    plt.xlim(0,xmax)
    plt.ylim(0,xmax)
    plt.legend(loc='best')
    plt.show()
    
    
if __name__ == '__main__':
    plotFeasibleTradingCurves(0.5,0.5)
    plotFeasibleTradingCurves(0.7, 0.3)