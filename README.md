# african-violence
Code to create networks based on the ACLED data.

Codebook: http://www.acleddata.com/wp-content/uploads/2016/01/ACLED_Codebook_2016.pdf

If you get an 'isinstance' error, replace the existing gml.py with the gml.py from Justin Ruths in the 'site-packages/zen/io' directory. (email dated 9 April)

##THINGS WE CAN DO:
- For the two graphs: Event count network, Fatalities network
    - Find degree distribution, does it follow a power law?
    - Diameter for the giant component
    - Degree / Eigenvector centrality (parties most involved in conflict)
    - Find modularity value for the different classes (e.g. civilians vs. non-civilians, Govt vs rebels)


## Actor Categories
All actors fall into 1 of 8 categories:
Government or mutinous force = 1
Rebel force = 2
Political militia = 3
Ethnic militia = 4
Rioters = 5
Protesters = 6
Civilians = 7
Outside/external force (e.g. UN) = 8
