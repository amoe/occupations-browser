# OCCUBROW roadmap

Estimated with a top-end velocity of 18 points a sprint.

## Around tasks (can be done at any time)

* Produce prototype in XD or Figma -- Not sure if this will be useful but it's
worth a try.  Figma has the advantage that it will be shareable using only
browser.
* Fix toolchain.
* Comparison with existing tools.
Cytoscape / Infranodus / Sigma / Rhodonite / Textexture / Recogito

## Part 1: Getting realistic inputs

* Representation of co-occurrence weights
** This overlaps with the one below.
* Feeding the tool from a raw corpus (that hasn't been de-duplicated)
* Link from data view back to source texts

To get the weights, we need to operate on the raw corpus.  We need to also
figure out how to STORE the weight in neo4j, and how to represent them on the
frontend.  (JS-level representatino & visual representation.)

The reason why we have to do this first is that the tool itself is performance
sensitive.  We have to be careful that we don't end up designing a tool
that becomes unusably slow with real data.

Generate small / medium / large version of 2 different corpora to test different
performance conditions based on data size.

Presentation points: TBC

## Part 2: Taxonomical extension

* Parsing existing taxonomies -- demonstrate this in presentation.
** How to visualize existing parse tree?  Open UI question
** Neo4j representation of taxonomy, demonstrate this is natural for N4J
* Filtering of view by taxonomized data
* Import of the Booth-Armstrong taxonomy
* Create pre-taxonomized token data -- 'naive taxonomization'
* Mostly grunt work

This has to be done before part 3, I think, because the concept of exporting
will be contingent on taxonomized annotations, ie it doesn't make sense to say
"export my edits/useful work I've done with the tool" without being able
to export taxonomical assignments.  (AB confirm?)

Presentation points: TBC.  Neo4j suitability for taxonomy approach relative to
relational approaches.  Existing critiques of taxonomy (linnaean etc)

## Part 3: Data model & data operations

* Implementation of split / join / grouping operators
** This is the key point of the annotation
** An exportable representation needs to be designed
** Needs to be end-to-end tested as designed: make operation, ensure that operation
has a reasonable export representations
** This is the key function that drives the rest of the data model and data model
may change after this step
** But previous data representations will be very simple so should be derivable
** Traditionally (in the non-graph world) it works the other way: the data model
drives the rest of the design

Presentation points:
* Discuss flexibility of graph DB schema design and the imperatives of 
query-based design
* What implications from graph theory are there (if any)?
-- Graph algorithms: minimum spanning tree (with inverted weights)
* Compilation of text / humanities operations to Cypher
* Relation to text-as-graph literature (dekker/birnbaum & others)

## Part 4: Cleanup, UI design, presentability

* Graph needs to look much prettier.  Take design cues from N4j browser, Gephi,
  force-directed, etc.
Concern with Fruchterman-Reingold is that it may be too slow.  However D3 does it
See if we can drop to raw-JS for layout efficiency.  GSAP for animations.
* The radial dendrogram -- justification of this in the presentation.
* The notion of the 'cognitive zoom' and re-centring.

The conference takes place on the 18th January 2019.

We want to leave an amount of time.  So our deadline is the 10th
January -- by then we want to have presentation finished, fully tested version
deployed, video made of the interaction, website published.

22 days in Nov + 15 days in Dec + 8 days in January = 45 days
81 points of complexity total capacity
4 and a half sprints.


Important thing to remember is that we can ALREADY do the lookup-by-semtag thing
a variation of it with the existing data on 'samdist.solasistim.net'

REferences

The NAHR paper

"The second category is a broader non- expert audience: the tool is also designed
to attract funding for the project, and interest for the digital humanities
field in general.  In that aspect, the interface should be viewed as usable and
fun by non-domain users" -- yuck

"For 8 out of 11 persons surveyed, we found that a tool allowing to visualize
groups of less than 50 persons at once was sufficient."  -- This is interesting
work from the UX perspective.

it appears to be a consensus that the field of digital humanities is "as buoyed
by optimism as it is laden with skepticism"
