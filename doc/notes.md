2019-01-04

going to neo4j

MATCH p = (n1 {content: "St."})-[r:PRECEDES*..4]->(n2) 
RETURN p;

MATCH p = (n1 {content: "St."})-[r:PRECEDES*]->(n2) 
RETURN n2, last(r).occurrences;


This is going to get the tree from thing.


            :fill="nodeFill[index] || defaultColor"


Action items list from alex:

* Relative proportion of size of taxons to indicate size
* Shading of taxons to indicate co-occurrence strength
** This requires returning occurrence data SOMEHOW to the API.
** This might need prototyping in python
* Radial bands shading
* Re-centre of nodes with animating nodes to new re-centered layout
* Pick a random node as root to begin with?
* Depth limitation
* Animate nodes to new re-centred layout
* Mock-up visuals for compound / group operations on a branch
* Create a taxonomization relationship by dragging to widget























































2019-01-03

Get all sentences tagged with the 'Manage' taxon.

MATCH (ta:Taxon {uri: "tag:solasistim.net,2018-12-28:occubrow/Manage/1"})<-[:INSTANCE_OF]-(to:Token)<-[:CONTAINS]-(s:Sentence)
RETURN s;


Now imagine that we want to return the tree rooted at these sentences.

We have to determine several things

There could be multiple roots, in fact there often will be this is the entire
point of a taxon; but since each token is identified once... We need to think
about cardinality problems.

simplify problem

2019-01-02

Now imagine that we have a path.  Such a path names a Taxon node with
specificity.  It will actually refer to its uri.  We will need to be able to get
the defined path of our URI.  We want getQuery() to be returning the uri.



























BLAH

Question being: How do I get the list of anything, for each taxon-selector?


2018-12-31

Need to check out the values from findvalidchildren.




















when we add a compound widget we have an error, can't happen
this is caused by the following
in compound widget
it goes to the taxon selector, getTaxonsByCompoundWidgetIndex

this goes to the condition if taxonomyType is null.

think about it
what is this lookup function gettings called with
is it correct?
it gets asked for display info for widget 0
why?
actually this makes sense because this is CW 0, not TS 0.
taxonomyref is clearly null.
this function is in util
makeemptycompoundiwdget

it can only be caused by the v-for
taxonIndices
taxonIndices should be returning an empty list but is not

remember this is based on taxons, so these will be calculate dbefore
do we have some circularity here


now the problem is that the empty widget is addd with 'hasLastEditableTaxon' as
true.  But that's not actually the case.

this will also need special handlers.


Also the available set needs to be passed in.

filteredChildren?


2018-12-29

mark up other things in document


































2018-12-27

"keep the St. Andrew, public-house, Gower-street, Portman-square"
"Tapster"
"drive the waggon"
"keep a shop for selling all sorts of wearing apparel"
"take bricks for him to different places"

We can manually create tags in the database by tagging all things of a certain kind.

occupation / object / place


what would that be?   place = {public-house, Gower-Street, Portman-square}


Occupation = {Tapster}

object = {waggon, shop, apparel, bricks}


Unfortunately since this doesn't have multiple levels, it doesn't demonstrate
the taxonomy in any reasonable way.

















2018-12-24

tree_data is using a special dfs method this seems to work ok


2018-12-10

  <svg xmlns="http://www.w3.org/2000/svg"
       :width="dynamicWidth" class="distance-indicator" ref="distanceIndicator">
    <line v-for="n in distance"
          :x1="getXPos(n - 1)" y1="0" :x2="getXPos(n - 1)" y2="100" :stroke="stroke"
          :stroke-width="strokeWidth"/>
  </svg>


2018-12-08

    <div>
      <div v-for="item in filteredChildren">
        <input type="radio" name="taxon" :value="item.model.id" 
               v-on:change="onSelect"/>
        <label :for="item.model.id">{{item.model.content}}</label>
      </div>
    </div>




2018-12-06


An issue here is that we can't just enumerate those things at level x, we really
need it to depend on the existing path-so-far

The toggle buttons will end up looking something like this:

        
        <ol>
          <li v-for="n in depth + 1">Toggle</li>
        </ol>


How we're going to filter it is pretty not clear.  It's obvious that given a 
Node, we can get the children of that node.  How can we look up a given node?
The question doesn't make sense, because every node retains its children.

We don't have networkx like lookup concepts, so we'll just have to walk the
tree.  We can do BFS search on the tree and at every concept we decrement our
path-so-far.  Each node BEEN having an identity.  So we just make sure that the
generated path contains the unique ID.  We obtain a list of IDs from the
selected filters so far.  Given this list of IDs -- which forms a path -- we can
find all direct children.

This can be tested, even.









2018-11-27

Trying to figure out what an input/output format would like for the OCCUBROW
tool.  There are various existing web standards that relate to this task.
Mostly XML-based.  OWL is an ontology description standard that can be used to
represent taxonomies.  I have written a taxonomy-importer from OWL that could be
used in a pinch.

The real question is how to represent annotated text and how to link it to
existing taxonomies.  To annotate a token as belonging to a certain taxon, you
need to know which taxonomy you're referring to.  So the URL of an OWL file
provides a nice way of making this link.  Any annotation that gets applied to a
token needs to be *symbolic*, that is, we can't simply use the
English-description of a taxon as the identifier, because we need something
unique.  One way is that every taxon can be assigned a UUID.  Alternatively, a
full path within the taxonomy tree could be used.  Both of these options are quite
verbose.  Another way would be to disambiguate duplicated names with a small numeric
suffix or something similar.

The innovation in this tool is specifically the graph view and operations.  I
hoped to use a standard method of import/export.  However every tool I could
find uses its own format.  For instance, brat uses a format described here:
http://brat.nlplab.org/standoff.html, while Sheffield's GATE tool uses two
formats, one extremely implementation-specific Java serialization and one rather
ad-hoc XML serialization that uses OWL URLs.  The rest of the semantic web
ecosystem is -- let's say -- rather a niche interest -- I wish I had the
knowledge of the ins and outs of it already, but I'm not sure I have time to
acquire it now, and something more hacky might be in order.

From a practical perspective we want to be able to share and import previously
annotated texts.  What I'm considering is perhaps 1) requiring UUIDs for nodes
during import 2) using a hash of the entire graph in the document header and
3) introducing redundancy by providing a UUID=>taxon-name mapping within the
file itself.  That way the exported document can seem to 'know' which taxonomy
it refers to but still retains the ability to be re-matched against any updates
that could happen.

2018-11-21

So we need some way to produce an Importable / Exportable Set

This is tricky

The Importable Set needs to be produced first.

It's obvious that 

https://www.npmjs.com/package/amoe-butterworth-widgets


























2018-11-20

killbox for each level

Plus should only appear on the final (lowest) taxonomy level and should be greyed
out if there are no taxonomy levels remaining
Kill button top left

Shade
Plus button forms the last pulse and pulses remain below

Adding 'floating' widget with plus button causes it to be untagged and shown
with border.  Can be moved into a category of taxonomical types.  Then it 
merges into a compound widget.

Grabbing entire groups and dropping and rearranging them: This means grabbing by
taxonomy type.

Also dragging should be restricted to within a certain vertical range.

distance + kind of distance

semantic data management -- check out timbuktoo

archers

metaphacts

https://www.archesproject.org/

2018-11-15

Widget birth spec: One row representing the taxonomy type
One row representing the level
A series of 'pulses' -- icons for these?
A button on the widget itself that adds a new widget IN THAT TAXONOMY TYPE

All widgets for a given taxonomy type are grouped, with a certain bracket
When one widget is dragged onto another widget, the top first level widget
'absorbs' the lower level widget
The filter-meaning is absorbed into it and the glyph disappears.
When I want to edit, I toggle a particular level by clicking the level-indicator
This will pop-out the other levels, shunting other type-brackets down the line
(Other ones that are shunted down the line will just occlude off the screen)

The blank widget button still exists

Speccing for next sprint:



























































2018-11-14

Having done the proof of concept for the taxonomy export root finder.  The next
step is to actually find out how to export the taxonomy.  Only then can the widgets
load it.




When we need to mock out the interface, we need to use MagicMock to mock the session

    mock_driver = unittest.mock.Mock()
    mock_session = unittest.mock.MagicMock()
    mock_driver.session.return_value = mock_session
    mock_session.__enter__ = lambda self: self
    mock_session.run.return_value = 42



2018-11-13

First goal: Export taxonomy
Problem: Need to specify taxonomy root in order to export a tree.
Question: How to specify taxonomy root?
Attempt: Specify by string name.
Problem: Does not uniquely identify node.
Question: How to uniquely identify node?
 {
   Attempt: Use UUID.
   Problem: Makes it hard to test.
   Answer: Mock UUID generator.
   Problem: Makes it hard for user to specify taxonomy.
   Answer: ??? Entails same code as below solution
  }
  {
  Attempt: find all valid roots at runtime and match string
  Problem: can we enforce at database level?  would entail in-degree constraints
  Answer: Use constraint?
  }
}

When we parse taxonomies, we should make sure that we aren't using 

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
