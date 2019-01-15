MATCH (st:StopWord)
WITH COLLECT(st.content) as stopWords
CALL algo.closeness.stream('Token', 'PRECEDES')
YIELD nodeId, centrality
WITH algo.getNodeById(nodeId).content as token, centrality
WHERE NOT token in stopWords
RETURN token AS node, centrality
ORDER BY centrality DESC
LIMIT 10;


Data layer needs to be refactored to encapsulate a custom data function

      <div class="sidebar">
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non tempor mi, vitae blandit erat. Curabitur felis mauris, aliquet vel congue sit amet, scelerisque ac turpis. Phasellus scelerisque ipsum sed lorem posuere, ultricies rutrum metus eleifend. Cras non enim non sem ornare facilisis condimentum vitae diam. Donec sit amet quam feugiat, interdum tortor id, fermentum lorem. Pellentesque quis ullamcorper diam, ut lacinia ipsum. Duis vel ultrices ligula.</p>
        <p>Proin tristique hendrerit lorem. Morbi aliquet sodales efficitur. Pellentesque imperdiet felis eros, at ultrices nunc dignissim at. Fusce non tristique augue, in interdum magna. Maecenas rhoncus ex eros, sed suscipit quam elementum eget. Maecenas vitae tincidunt eros, ac volutpat turpis. Curabitur imperdiet ut quam nec suscipit. Donec commodo ex convallis justo rhoncus, at vehicula ex dapibus. Fusce pellentesque arcu ac viverra interdum.</p>
        <p>Quisque urna turpis, sodales ac vulputate at, pharetra sed turpis. Mauris maximus efficitur cursus. Aenean ullamcorper nunc non ipsum fermentum gravida. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In hac habitasse platea dictumst. Quisque euismod lectus ac neque tincidunt, quis auctor augue feugiat. Sed ac leo egestas, suscipit sapien ut, blandit nibh. Duis malesuada tempus hendrerit. Phasellus pulvinar ullamcorper faucibus.</p>
      </div>

<circle r="16" cx="0" cy="0" opacity="0.2" class="ghost-node" 
        data-svg-origin="-16 -16" transform="matrix(1,0,0,1,0,0)"
        style="cursor: move; touch-action: none; user-select: none; z-index: 1000; transform: matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 39, 125, 0, 1);"><title>a</title></circle>

Presentation outline

Data model data models 
Vue implementation
notes on the implementation of graphs
centrality measure and the thing
licensing and technology

Fix clicking and pressing enter on buttons
Fix heightened window
Taxonomy spec being wiped on drag
Set serif to be closed by default
Snap back shadows and do not register click
Fix "no root somehow"
Loading spinner
Filtering large trees

Narrow the data to the available stuff based on patterns from occupation csv.

<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non tempor mi, vitae blandit erat. Curabitur felis mauris, aliquet vel congue sit amet, scelerisque ac turpis. Phasellus scelerisque ipsum sed lorem posuere, ultricies rutrum metus eleifend. Cras non enim non sem ornare facilisis condimentum vitae diam. Donec sit amet quam feugiat, interdum tortor id, fermentum lorem. Pellentesque quis ullamcorper diam, ut lacinia ipsum. Duis vel ultrices ligula.</p>

<p>Proin tristique hendrerit lorem. Morbi aliquet sodales efficitur. Pellentesque imperdiet felis eros, at ultrices nunc dignissim at. Fusce non tristique augue, in interdum magna. Maecenas rhoncus ex eros, sed suscipit quam elementum eget. Maecenas vitae tincidunt eros, ac volutpat turpis. Curabitur imperdiet ut quam nec suscipit. Donec commodo ex convallis justo rhoncus, at vehicula ex dapibus. Fusce pellentesque arcu ac viverra interdum.</p>

<p>Quisque urna turpis, sodales ac vulputate at, pharetra sed turpis. Mauris maximus efficitur cursus. Aenean ullamcorper nunc non ipsum fermentum gravida. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In hac habitasse platea dictumst. Quisque euismod lectus ac neque tincidunt, quis auctor augue feugiat. Sed ac leo egestas, suscipit sapien ut, blandit nibh. Duis malesuada tempus hendrerit. Phasellus pulvinar ullamcorper faucibus.</p>

<p>Etiam ac rutrum mi, vitae efficitur nibh. Pellentesque faucibus ante lacus, et ornare sapien dictum quis. Phasellus euismod sodales convallis. Pellentesque vitae lectus a elit vestibulum dignissim. Suspendisse condimentum venenatis tristique. Maecenas egestas condimentum neque, nec tincidunt sapien consectetur quis. Sed gravida dui vitae ex sagittis, posuere mollis ante consectetur.</p>

<p>Nulla gravida lorem quis mollis molestie. In id congue leo, vel fringilla leo. Ut urna mi, venenatis in dui vel, placerat tempus tellus. Aliquam ligula nisl, volutpat eget sem hendrerit, dictum tempus felis. Cras in hendrerit quam, vitae dictum nisi. Sed mollis dolor in enim efficitur venenatis. Nam eleifend dictum bibendum. Phasellus varius imperdiet euismod.         </p>




<div class="page">
    <widget-view :taxonomies="taxonomies" ref="widgetView"></widget-view>

  <el-main>
    <el-popover placement="bottom"
                :title="popoverTitle"
                width="200"
                trigger="manual"
                v-model="popoverVisible">
      <div v-for="sentence in displayedContexts">
        <span v-for="token in sentence.content">
          <span v-on:click="recenter(token)"
                class="context-token">{{token}}</span>&nbsp;
        </span>
      </div>
    </el-popover>

    <svg id="svg-frame" :width="width * 2" :height="height">
      <graph-view v-if="isDataLoaded"
                  v-on:node-clicked="handleNodeClicked"
                  :graph-data="graphData"
                  :width="width"
                  :height="height"
                  :x-margin="162"
                  :y-margin="0"
                  :depth-offset="120"
                  :text-offset="22"
                  :text-content-template="textContentTemplate"
                  :breadth="360"
                  ref="graphView"></graph-view>
    </svg>
  </el-main>

  <el-footer>

  <el-select v-model="chosenRoot"
             id="root-selector"
             filterable
             remote
             placeholder="Please enter a keyword"
             :remote-method="remoteMethod"
             :loading="loading">
    <el-option v-for="item in filteredTokenSelection"
               :key="item"
               :label="item"
               :value="item">
    </el-option>
  </el-select>

    <div v-if="metrics">
      <span>Order: {{metrics.order}}.</span>&nbsp;
      <span>Size: {{metrics.size}}.</span>&nbsp;
      <span>Depth limit: {{depthLimit}}.</span>
      <!-- can't list max depth yet due to some communication problems -->
    </div>
    AGPL 2019
  </el-footer>
</div>































MATCH (ta1:Taxon)
OPTIONAL MATCH (ta1)-[:SUPERCATEGORY_OF*]->(ta2:Taxon)
WHERE ta1.uri IN []
WITH [] + COLLECT(ta2.uri) AS validTaxonUris
MATCH (to1:Token {content: "Andrew"}), (to1)-[r:PRECEDES*..10]->(to2:Token)
WITH to1 AS to1, to2 as to2
MATCH (to3)-[:INSTANCE_OF]->(ta:Taxon)
WHERE ta.uri IN []
RETURN COLLECT(to1) + COLLECT(to3) AS nodes, [] AS rels

there is some problem here the problem being that the WHERE clauses just filters
rows meaning that we don't get any returns for an empty graph.

MATCH (to:Token {content: "keep"})<-[:CONTAINS]-(s:Sentence)
RETURN s


WITH ["tag:solasistim.net,2018-12-28:occubrow/Vehicle/1", "tag:solasistim.net,2018-12-28:occubrow/Bricks/1"] AS l
MATCH (ta:Taxon)
WHERE ta.uri IN l
RETURN ta;


MATCH (to1:Token {content: "keep"}),
      (ta:Taxon {uri: "tag:solasistim.net,2018-12-28:occubrow/Vehicle/1"})
OPTIONAL MATCH (to1)-[r:PRECEDES*..4]->(to2:Token)
WHERE ANY((to2)-[:INSTANCE_OF]->(ta)
RETURN (COLLECT(to1) + COLLECT(to2)) AS nodes, COLLECT(last(r)) AS rels

MATCH (to1:Token {content: "keep"}),
      (ta:Taxon {uri: "tag:solasistim.net,2018-12-28:occubrow/Vehicle/1"})
OPTIONAL MATCH (to1)-[r:PRECEDES*..4]->(to2:Token)
WHERE (to2)-[:INSTANCE_OF]->(ta)
RETURN (COLLECT(to1) + COLLECT(to2)) AS nodes, COLLECT(last(r)) AS rels




thinking about this

we can do the simplest thing


Alex wrote this...
    OPTION ONE

    The ego node represents an arbitrary (or pre-determined) token

    The first taxon-selector (in widgets bar) determines the taxon-type for the first ring of nodes
    > The first ring of nodes displays all tokens that are currently assigned to that taxon (which co-occur in a sentence with the ego-node-token)

    On selection of a second taxon-selector, this determines the taxon-type for the second ring of nodes
    > The second ring of nodes displays all tokens that are currently assigned to that taxon (which also co-occur in a sentence with both the ego-node-token and a token on the first ring)
    Each token on the second ring sits on a path connecting it to the token on the first ring with which it co-occurs

    Nodes are shaded according to the relative frequency with which they co-occur either (a) with the immediately preceding token, or (b) with all the tokens preceding it on the path

    Etc.

    OPTIONS TWO (a and b)

    The ego node represents an arbitrary (or pre-determined) token

    The first taxon-selector (in widgets bar) determines the first taxon-type
    > The paths outwards from the ego node represent tokens that occur in the same sentence as the ego-node-token and the first-taxon-selector taxon
    These are filtered as (either):

    (a) all tokens that occur in sentences that include a token with this taxon-type: these sit on the radiating paths according to the sequence of their co-occurence/connections
    Or
    (b) all tokens that have been assigned taxons, which are placed on the first ring, with no other tokens visible

    Etc.
    OPTION THREE

    A taxon is selected in a first taxon selector
    > The ego node represents the first selected taxon in the widget bar

    A taxon is selected in a second taxon selector
    > The first ring of nodes represent all the tokens-assigned that taxon that co-occur in a sentence with the Ego-node-taxon, and all the sub-taxons (i.e. tokens ‘grouped’ as that sub-taxon)
    > where sub-taxons occur, the second ring represents the tokens ‘grouped’ in these sub-taxons

    Etc
    There you go! TO DISCUSS!

I wrote this...
Alex was describing a situation of what happens when you have 2 filters, one for
'vehicle' and one for 'street'

At present, let's say the ego node is rooted at token 'keep'

The depth limit is defined to 4 by the user.

if we go with the most obvious current interpretation, then we first restrict
all Token nodes displayed to be those which have been assigned to taxon Vehicle
(or its sub-taxons), and then addtionally show nodes that have been assigned to
taxon Street (or its sub-taxons), in ANY SENTENCE but within the depth range of
4, so they all have to co-occur within that limit, [whether the intervening
nodes on the traversed paths that didn't match the filters are kept or displayed
in any way is unclear].  Adding filters initially decreases the amount of data
shown and each additional filter forms an 'OR' condition, so expands the data
shown

if we go with another (foolish) interpretation, adding 2 filters restricts the
view to only Token nodes which have been classified as both Vehicle and Street,
but there wouldn't be many such nodes.

if we go with another interpretation, adding the first filter 'vehicle' forms a
filter on the SENTENCES that are considered to be shown in the graph instead.
Adding street restricts this set further that the set of sentences has to
include both vehicle and street (but they can occur anywhere in the sentence,
even past the depth limit of 4).  However this raises the question of what to do
with the ego node, which still has the token 'keep'.  Under the current
implementation, all candidate sentences would also have to contain 'keep' (and
this would have to be BEFORE the specific vehicle or street tokens).  which is
slightly strange behaviour.

The idea of a 'root' Token node could be discarded.  In that case we'd have a
set of trees displayed instead of just 1 tree.  However, then the concept of
re-centring 'on' a node doesn't make obvious sense any more.  At least it
doesn't make sense as 'exploring' the corpus, because you can't easily move back
and forward, how would you be able to describe the state 'before' re-centring?








https://stackoverflow.com/questions/44119453/neo4j-shortestpath-with-highest-aggregated-relationship-propertie

What do we expect in the case where we filter.

The result of this is that the final path element should be expanded.
Do this as a parameter to the path expander?

We still need to take the root into account.

MATCH (to1:Token {content: "keep"}), (ta:Taxon {uri: "tag:solasistim.net,2018-12-28:occubrow/Vehicle/1"})
OPTIONAL MATCH (to1)-[r:PRECEDES*..4]->(to2:Token)
WHERE (to2)-[:INSTANCE_OF]->(ta)
RETURN (COLLECT(to1) + COLLECT(to2)) AS nodes, COLLECT(last(r)) AS rels

this clear nonsensical relation


beware that using the path expander might be necessary


Do list from below:

https://www.reddit.com/r/webdev/comments/aehxc7/what_are_some_easysmall_things_that_you_do_that/

MATCH (t:Token) WITH t WHERE rand() < 0.3 RETURN t LIMIT 1;

Main Action Items Left 2019-01-10:

* Restrict tree to top N
* Pick a random node as root to begin with?
* Mock-up visuals for compound / group operations on a branch
* Create a taxonomization relationship by dragging to widget
* Create source text link back to sentence
* Show metrics from node
* Allow filtering tree by taxon

Not possible to create indices on relationship properties

apoc.path.subgraphAll

apoc.path.subgraphAll(
startNode <id>Node/list, {maxLevel, relationshipFilter, labelFilter, bfs:true, filterStartNode:true, limit:-1}) yield nodes, relationships



maximum cooccurrence value

MATCH (to1:Token {content: "keep"}) OPTIONAL MATCH (to1)-[r:PRECEDES*..4]->(to2:Token) WHERE r.occurrences > 10 RETURN COUNT(DISTINCT to1) AS count1, COUNT(DISTINCT to2) AS count2, COUNT(DISTINCT r) AS count3; 

MATCH (to1:Token {content: "keep"})
OPTIONAL MATCH (to1)-[r:PRECEDES*..2]->(to2:Token) RETURN COUNT(DISTINCT to1) AS count1, COUNT(DISTINCT to2) AS count2, COUNT(DISTINCT r) AS count3; 

MATCH (to1:Token {content: "keep"})
OPTIONAL MATCH (to1)-[r:PRECEDES*..3]->(to2:Token)
RETURN COUNT(DISTINCT to1) AS count1, COUNT(DISTINCT to2) AS count2, COUNT(DISTINCT r) AS count3;

This will give you an idea of what you can expect from the result graph

Verify your server configuration. For example, if you have large value for
org.neo4j.server.transaction.timeout and you don't handle properly transaction
at client side - you can end up with a lot of running transactions.


MATCH (to1:Token {content: "keep"})
OPTIONAL MATCH (to1)-[r:PRECEDES*..4]->(to2:Token)
RETURN (COLLECT(to1) + COLLECT(to2)) AS nodes, COLLECT(last(r)) AS rels

Create an index: `CREATE INDEX ON :Token(content)`.


* Store data set reference on the SENTENCE.  This needs to involve formalizing the prep step
* Store word count -- total number of times this token has been seen
* Query for word pairs collocations
* Import is SLOW
* Add index on URIs for taxonomies?
* Add index on content property?

challenges: making this usable large scale -- it's not practical for
users to import huge dbs -- we'd be eating insane memory
it's better for them to share imported corpora, like in SketchEngine

closeness centrality -- see https://www.aclweb.org/anthology/I/I13/I13-1102.pdf
this is used for some NLP

 Florian Boudin in "A Comparison of Centrality Measures for Graph-Based Keyphrase Extraction". 
irritating remaining points
error handling
listing of available taxonomies from server


2019-01-09

what needs to happen here
clearly the taxons can only have one content value
but their actual definitions are defined by their parents etc
they already have a format for producing tag URIs
because they have a unique identifier
so the uri identifier can encode the 00 category
content can contain the human readable description
the annotations then can be looked up with a search on content

the trouble is that taxonomyinserter contains its own code to generate URIs
this is a bit of a problem

in networkx, each node should have the URI as its node value, with the content specified
as an edge
then the taxonomy inserter just runs that

we write an adapter that uses make_tag_uri to tag up the example taxonomy
properly

so the next step is to modify the 









































j
depth = 0, y = 0
depth = 1, y = 90
depth = 2, y = 180



Radius is actually just the regular radius.
Find max depth in hierarchy

So the correct radius of circles is 
((width / 2) - depthOffset) / maxDepthInHierarchy

It simply divides all available space between max depth in a certain path.
If max depth in one direction is 1, the y value will be 180, so it will appear
symmetrical.

how to match entities that might be deeper in the graph?

william lyon, video
https://github.com/graphaware/neo4j-nlp

response to this article

https://neo4j.com/blog/bring-order-to-chaos-graph-based-journey-textual-data-to-wisdom/

Algorithms:
Centrality
Community detection
Path finding (random walk?)


The most important thing is to get the samuels taxonomy import going.

MATCH (to1:Token {content: "Portman-square"})
OPTIONAL MATCH (to1)-[r:PRECEDES*..2]->(to2:Token)
RETURN (COLLECT(to1) + COLLECT(to2)) AS nodes, COLLECT(last(r)) AS rels


    MATCH (to1:Token {content: "Portman-square"})-[r:PRECEDES*..2]->(to2:Token)
    RETURN (COLLECT(to1) + COLLECT(to2)) AS nodes, COLLECT(last(r)) AS rels


MATCH (ta:Taxon {uri: "tag:solasistim.net,2018-12-28:occubrow/Manage/1"})<-[:INSTANCE_OF]-(to:Token)
WITH DISTINCT to AS roots
MATCH (to)-[r:PRECEDES*..4]->(to2:Token)
RETURN (COLLECT(to) + COLLECT(to2)) AS nodes, COLLECT(last(r)) AS rels;

I mean this is a problem, because we only see a certain thing


lessons:

n4j python had to read the source a lot
Large JS is very difficult to manage
Typescript helps a lot
However typescript can introduce its own difficulties
circles need to adjust to the base stuff properly
The space of Neo4j is poorly theorized compared to RDBMS wrt best practices
For such a common feature, drag and drop is very poorly specified
Testing for multi lang projects is hard

2019-01-08

Remember that the circle will always be at the centre.

So imagine just steadily increasing the radius.

180 is the max radius

2019-01-07

Problem now becomes that we can no longer use rebuild_graph to do the
needful -- WHY -- because it's reliant on a different data shape.

The 'shim_subgraph_result' relies on being able to return lists with
values nodes and rels

Can we get our data into this format?

MATCH (to1:Token {content: "keep"})-[r:PRECEDES*..2]->(to2:Token)
RETURN COLLECT(to1) + COLLECT(to2), COLLECT(last(r)) AS r2;

    for row in r:
        r = row.value('r')
        to1 = row.value('to1')
        to2 = row.value('to2')

        strength = r['occurrences']

        print("to2 has strength", r['occurrences'])

        g.add_node(to1['content'])
        g.add_node(to2['content'], strength=strength)

        g.add_edge(to1['content'], to2['content'])





















j

What is the needful??  Calculate strength and embed it into node response
This involves updating tests for get_tree backend API.


How are we actually going to do the events?

We probably need to emit a sensible semantic event to the upper layer that
is going to communicate the change.  HOW DOES THIS WORK -- custom events.




2019-01-07

            // Now we know what nodes are old.

            this.tweenedHierarchy = cloneDeep(newData);   // or clone, or just assign

            // Old nodes start at their old positions.

            this.tweenedHierarchy.

            const nodesToBeTweened = this.tweenedHierarchy.descendants();

            for (let node of nodesToBeTweened) {
                if (oldTokenSet.has(node.data.content)) {
                    const targetX = node.x;
                    const targetY = node.y;

                    TweenLite.to(node, 0.5, {x: targetX, y: targetY});
                }
            }


The problem is that new stuff should go there immediately, while the old nodes
should have their old positions.

so we have a computed property that watches the 
graphDataFromStore property


                function (node: HierarchyNode<TokenDatum>): string {
                    return node.data.content;
                }


            const commonNodes = intersectionBy(
                oldData.descendants(), newData.descendants(),
                n => n.data.content
            );

            const oldNodeSet = new Set(commonNodes);

            console.log("Common nodes are %o", oldNodeSet);

            this.tweenedHierarchy = newData;






































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
* Depth limitation
* Animate nodes to new re-centred layout






















































2019-01-03

Get all sentences tagged with the 'Manage' taxon.

MATCH (ta:Taxon {uri: "tag:solasistim.net,2018-12-28:occubrow/Manage/1"})<-[:INSTANCE_OF]-(to:Token)
WITH DISTINCT to
RETURN to


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
