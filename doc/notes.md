2018-11-13

The outcome of this was that  GATE support ontology import in the format OWL-lite.
It supports exporting either in GATE format which is a proprietary set of nodes:

    <?xml version='1.0' encoding='UTF-8'?>
    <GateDocument version="3">
    <!-- The document's features-->

    <GateDocumentFeatures>
    <Feature>
      <Name className="java.lang.String">gate.SourceURL</Name>
      <Value className="java.lang.String">created from String</Value>
    </Feature>
    </GateDocumentFeatures>
    <!-- The document content area with serialized nodes -->

    <TextWithNodes>The <Node id="4"/>wildehaard<Node id="14"/> did a blunderbaard on the <Node id="41"/>PDP-11.<Node id="48"/></TextWithNodes>
    <!-- The default annotation set -->

    <AnnotationSet>
    </AnnotationSet>

    <!-- Named annotation set -->

    <AnnotationSet Name="dave">
    <Annotation Id="0" Type="Mention" StartNode="4" EndNode="14">
    <Feature>
      <Name className="java.lang.String">class</Name>
      <Value className="java.lang.String">http://gate.ac.uk/owlim#animal</Value>
    </Feature>
    <Feature>
      <Name className="java.lang.String">ontology</Name>
      <Value className="java.lang.String">http://gate.ac.uk/owlim</Value>
    </Feature>
    </Annotation>
    <Annotation Id="1" Type="Mention" StartNode="41" EndNode="48">
    <Feature>
      <Name className="java.lang.String">class</Name>
      <Value className="java.lang.String">http://gate.ac.uk/owlim#computer</Value>
    </Feature>
    <Feature>
      <Name className="java.lang.String">ontology</Name>
      <Value className="java.lang.String">http://gate.ac.uk/owlim</Value>
    </Feature>
    </Annotation>
    </AnnotationSet>

    </GateDocument>

Or it supports exporting in an inline-annotation format which depends upon
defining the Annotation Set.


    The <Mention gate:gateId="3" class="http://gate.ac.uk/owlim#animal"
    ontology="http://gate.ac.uk/owlim">wildehaard</Mention> did a blunderbaard on
    the <Mention gate:gateId="4" class="http://gate.ac.uk/owlim#computer"
    ontology="http://gate.ac.uk/owlim">PDP-11.</Mention>

GATE
see this https://gate.ac.uk/sale/talks/gate-course-aug10/track-3/module-9-ontologies/module-9-ontologies.pdf

the other thing is Protege
https://protege.stanford.edu/
Not NER - - flat structure
https://gate.ac.uk/sale/talks/gate-course-aug10/track-3/module-9-ontologies/module-9-ontologies.pdf

Semantic annotation 
– annotate in the texts all mentions of 
instances relating to concepts in the ontology
Magpie, firefox plugin from Open University
OAT (Ontology Annotation Tool)

Thisis  a GATE plugin

https://gate.ac.uk/sale/tao/splitch14.html
COllaborative a la Brat
https://pypi.org/project/Owlready2/

WSD as token -- all tokens are identical  although instances can be distinguished



2018-11-09




We can't figure out how to get the 


MATCH (t1:Token {content: "nonexistent"})-[r:PRECEDES]-(t2:Token {content: "nonexistent"}) SET r.occurrences = r.occurrences + 1;

CREATE (t1:Token {content: "foo"})-[:PRECEDES {occurrences: 1}]->(t2:Token {content: "bar"});


MATCH (t1:Token {content: "foo"})-[r:PRECEDES]-(t2:Token {content: "bar"})
RETURN r.occurrences;

MATCH (t1:Token {content: "foo"})-[r:PRECEDES]-(t2:Token {content: "bar"})
SET r.occurrences = r.occurrences + 1;

MATCH (t1:Token {content: "nonexistent"})-[r:PRECEDES]-(t2:Token {content: "nonexistent"}) SET r.occurrences = r.occurrences + 1;


for phrase in phrases:
    first_idx = 0
    last_idx = len(phrase) - 1
    
    for index in range(last_idx):
        print(phrase[index])
        print(phrase[index + 1])






2018-11-08

        cypher_params = {
            'statement': "CREATE (t:Taxon $properties)",
            'parameters': None,
            'kwparameters': {
                'properties': {
                    'content': taxonomy_data['id']
                }
            }
        }
        
        self.repository.run_statement(cypher_params)





Now that we own the N4J interface, we need to be able to declare what database
structure we want to get after the import happens, but in order to do that
we need to be extracting the graph labels as well as the properties.

The tarfile doesn't open successfully, so maybe it didn't download the first time

* Modify node
* Extract label from node

A node can have multiple labels; but perhaps we just don't support that use-case

So whatt about 'prepared statements'



























2018-11-07


We have an issue because we don't 'own' the n4j interface.  It's difficult to
mock out comfortably because our backend class calls things on it directly.
It returns objects that are not "plain old objects" essentially.  We'll have
to add a translation layer to convert it to our own objects.

We need two classes, Node and Relationship, to fully reconstruct the tree.

Node needs two methods:
   get_id() => int
   get_properties() => dict

Relationship needs four methods:
   get_start_node() => int
   get_end_node() => int
   get_properties() => dict
   get_type() => str

pull_graph now returns a dict where the values are lists of Nodes and
Relationships.












































https://www.huygens.knaw.nl/timbuctoo/?lang=en
https://www.w3.org/TR/prov-o/
ontotext
data modelling
taxonomized data sets & taxonomies
biomedical engineering - ontologies
dbpedia -- DBpedia taxonomy / ontology

NER-tagged text & ontological assignment in Dbpedia
dbpedia python3 auto-classify

2018-11-06


assert_graph is going to check that the two graphs are isomorphic

MATCH ()-[r]->()
WITH COLLECT(r) AS rels
MATCH (n)
RETURN rels, COLLECT(n) AS nodes

CALL apoc.export.graphml.all('yourPath/exportAll.graphml',null);

NEO4J_TEST_PORT = 15374

bolt_port = NEO4J_TEST_PORT
bolt_address = ("localhost", bolt_port)
bolt_uri = "bolt://%s:%d" % bolt_address

realpath = boltkit.controller._install(
    edition='community',
    version='3.4.6',
    path="ext"
)
print("Initialized home at", realpath)
boltkit.config.update(
    realpath,
    {boltkit.config.BOLT_LISTEN_URI_SETTING: bolt_uri}
)

controller = boltkit.controller.create_controller(path=realpath)
instance_info = controller.start()
print("Instance info is", instance_info)
#driver = neo4j.GraphDatabase.driver(bolt_uri)
#controller.stop()


    # names = set()
    # print = names.add

    # def print_friends(tx, name):
    #     for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) "
    #                          "WHERE a.name = {name} "
    #                          "RETURN friend.name", name=name):
    #         print(record["friend.name"])

    # with driver.session() as session:
    #     session.run("MATCH (a) DETACH DELETE a")
    #     session.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")
    #     session.read_transaction(print_friends, "Alice")

    # assert len(names) == 1
    # assert "Bob" in names


2018-11-05

"Protocol family unavailable" on travis -- 

I ran into this in the process of setting up travis-ci; within its environments,
ipv6 :: is resolved, but cannot be bound. Fixed by 36c77dd.

Need to re-derive the integration test base case and reform it as neo4j.
