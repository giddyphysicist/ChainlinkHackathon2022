# ChainlinkHackathon2022
Chainlink Hackathon project 2022 -- Adaptive Market Maker


## Adaptive Trading Curves

A variation on the Constant-Product Market Maker (CPMM) theme, this project will prototype an exchange with tunable trading curves. 

That is, based on different market conditions, the exchange will alter the functional form of the bonding curve to more closely approach a linear curve, such as is done for stablecoin projects like Curve Finance, or to more closely approach the constant product xy=constant curve, or to more closely approach a function with even more curvature, as might be more appropriate for highly leveraged or extremely volatile assets.

## Chainlink Interfaces

We plan on leveraging Chainlink price oracles in tandem with Chainlink Keepers in order to regularly check the changes of market prices over a given period, and then automatically adjust the bonding curve to optimize for different trading and LP positions.

