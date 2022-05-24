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
                # if k**q < x**q, return nan.
                if (x**q > k**q):
                    yvec.append(np.nan)
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
    # qvals = [-0.8, 0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8]
    qvals = [-1.0, -0.5, 0.0, 0.5]
    plt.figure(figsize=(6,6))
    for q in qvals:
        k = calculate_k(q, xfraction * xmax,yfraction * xmax)
        y = calculate_y_vec(x, q, k)
        if np.isclose(q,0):
            plt.plot(x,y,'k--',label=f"q={q:3.1f} : xy=k (uni.)")
        else:
            plt.plot(x,y,label=f"q={q:3.1f}")
    plt.xlabel('Token X reserves')
    plt.ylabel('Token Y reserves')
    plt.xlim(0,xmax)
    plt.ylim(0,xmax)
    # plt.legend(loc='best')
    plt.show()
    
class Exchange():
    def __init__(self, x,y,q):
        self.q = Decimal(q)
        self.x = Decimal(x)
        self.y = Decimal(y)
        if np.isclose(float(q),0.0):
            self.k = self.x*self.y
        else:
            self.k  = (self.x**self.q + self.y**self.q)**(Decimal(1)/self.q)
        self.reserveHistory = [(self.x, self.y)]
    
    
    def __repr__(self):
        s = '\n'.join(["===== ADAPTIVE MARKET MAKER =====",
                       f"q = {self.q}",
                       f"x = {self.x}",
                       f"y = {self.y}",
                       f"k = {self.k}"])
        return s
    
    def updateQ(self, newq):
        self.q = Decimal(newq)
        if np.isclose(float(self.q),0.0):
            self.k = self.x*self.y
        else:
            self.k  = (self.x**self.q + self.y**self.q)**(Decimal(1)/self.q)
    
    def tradeXforY(self, dx):
        dx = Decimal(dx)
        newx = self.x + dx
        if np.isclose(float(self.q),0.0):
            newy = self.k / newx
        else:
            newy = (self.k**self.q - newx**self.q)**(Decimal(1)/self.q)
        dy = self.y - newy
        
        self.x = newx
        self.y = newy
        self.reserveHistory.append((self.x,self.y))
        return dy
       
    def tradeYforX(self, dy):
        dy = Decimal(dy)
        newy = self.y + dy
        if np.isclose(float(self.q),0.0):
            newx = self.k / newy
        else:
            newx = (self.k**self.q - newy**self.q)**(Decimal(1)/self.q)
        dx = self.x - newx
        
        self.x = newx
        self.y = newy
        self.reserveHistory.append((self.x,self.y))

        
        return dx
    
    def plotReserveHistory(self,ax):
        rh = np.array(self.reserveHistory)
        xvals = rh[:,0]
        yvals = rh[:,1]
        
        ax.plot(xvals,yvals,'o',alpha=0.3)
    
    
if __name__ == '__main__':
    pass
    ex = Exchange(1000000000, 1000000000, -0.5)
    dx = 10000000
    plt.plot(ex.x, ex.y,'go')
    for i in range(100):
        print(ex.tradeXforY(dx))
    ex.updateQ(0)
    plt.plot(ex.x, ex.y,'r^')
    ax = plt.gca()
    for i in range(100):
        print(ex.tradeYforX(dx))
    ax.plot(ex.x, ex.y, 'ks')
    ex.updateQ(0.5)
    for i in range(50):
        print(ex.tradeXforY(dx))
    ax.plot(ex.x, ex.y, 'kx')
    ex.plotReserveHistory(ax)

    

    # plotFeasibleTradingCurves(0.5,0.5)
    # plotFeasibleTradingCurves(0.7, 0.3)
