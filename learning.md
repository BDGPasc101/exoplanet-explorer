We use the streamlit package to display data from Nasa
- Streamlit uses inbuilt UI tools which is why research developers use it regularly
- Uses modern react.js web interface

Toggle to isolate earth-like planets
Physics:
 filtering for a Stellar Effective Temperature ($T_{eff}$) between 2,500 K and 6,000 K. This specifically isolates M, K, and G-type main-sequence stars.

 Added extra filter for distance from our system

Build earth similarity index using pandas function
The standard Earth Similarity Index (ESI) uses a mathematical concept called a distance metric. Because our dataset measures mass and radius in "Earth units" (meaning Earth = $1.0$), we can calculate the similarity for any property $x$ using this formula:
$$\text{Similarity} = 1 - \left\vert{} \frac{x - 1}{x + 1} \right\vert{}$$
If a planet's mass is exactly 1, the result is $1.0$ (perfect match). If it's vastly larger or smaller, it approaches $0.0$. We will calculate this for both mass and radius, and multiply them together for our final ESI score.

I want to be able to filter out volatile young stars, so I updated the fetch to get the star age

Was also showing too many planets which did not lie in habitable zones, so I've added this filter too
Result - out of the whole data set, it looks like only 2 planets are earth like candidates in habitable zones - TRAPPIST-1 e and GJ 1061 d

Ideas
- Use my study of galactic metallicity regions from my undergrad dissertation


