// create a taxo

CREATE (t1:Taxon {root: true, content: 'Occupation'}),
       (t2:Taxon {content: 'Manage'}),
       (t3:Taxon {content: 'Serve'}),
       (t4:Taxon {content: 'Drive'}),
       (t5:Taxon {content: 'Transport'}),
       (t1)-[:SUPERCATEGORY_OF]->(t2),
       (t1)-[:SUPERCATEGORY_OF]->(t3),
       (t1)-[:SUPERCATEGORY_OF]->(t4),
       (t1)-[:SUPERCATEGORY_OF]->(t5);


CREATE (t1:Taxon {root: true, content: 'Place'}),
       (t2:Taxon {content: 'Pub'}),
       (t3:Taxon {content: 'Shop'}),
       (t4:Taxon {content: 'Clothes shop'}),
       (t1)-[:SUPERCATEGORY_OF]->(t2),
       (t1)-[:SUPERCATEGORY_OF]->(t3),
       (t3)-[:SUPERCATEGORY_OF]->(t4);


CREATE (t1:Taxon {root: true, content: 'Object'}),
       (t2:Taxon {content: 'Alcoholic drink'}),
       (t3:Taxon {content: 'Vehicle'}),
       (t4:Taxon {content: 'Clothes'}),
       (t5:Taxon {content: 'Bricks'}),
       (t1)-[:SUPERCATEGORY_OF]->(t2),
       (t1)-[:SUPERCATEGORY_OF]->(t3),
       (t1)-[:SUPERCATEGORY_OF]->(t4),
       (t1)-[:SUPERCATEGORY_OF]->(t5);
