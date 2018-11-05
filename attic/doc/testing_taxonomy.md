Procedure:

* Load the demo data, 

    amoe@cslp019129 $ python3 scripts/import_data.py data/1-obo1674-1834_occupations_20180104.csv

Check localhost:7475

Assertions:
* MATCH (n) RETURN count(n) shoudl return 20980
* MATCH (t:Taxon) RETURN count(t) shoudl return 0

* Load the taxonomy,

    python3 -m scripts.load_demo_taxonomy

It's important that you run it with the `-m` syntax because this will set up
the PATH correctly.

* Randomly assign the taxonomy elements

    python3 -m scripts.randomly_assign_taxonomy_elements
