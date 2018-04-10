# OCCUPATION EXPLORER PROJECT

Now, it's slightly wrong to name this project the Occupation Explorer because it
slightly changed specification during this meeting.  Fundamentally it's a simple
query tool but also one that feeds data back to a process that can 
generate human-verified outputs that can be used for training models or for 
testing symbolic rules (that we devise).

The basic data layout is as follows:

At the top, the control bar: this is essentially a three column row.

We define 'the input' to be a set of 'job expressions'.   A 'job expression' is
a sequence of tokens.  The tokenization that's done is outside of the scope of 
this spec and may be controversial in itself.  See Note 1.

The input itself comes in the form

    input = List<JobExpression>
    typedef JobExpression List<Token>
    typedef Token String

So the input is essentially `List<List<String>>`.  We could hope to attach more
information to the individual tokens.  And in fact, this may be necessary, if we
hope to bundle further information with them, that would be preserved by the
structuring.  Imagine in TypeScript we could define a token as such:


    interface Token {
        content: string;
        attachment: object;
    }

(Note that in TS interfaces are more like structs than they are Java-ish
interfaces.)  Note that we don't specify the internal structure of the 
`attachment` member.  In this case it's just some arbitrary bundled data that
we receive from the client.

Once we receive the input, we do a processing step to transform each
JobExpression to a graph representation.  The list of all graph representations
of JobExpressions is called _G_.  You can think of the type of `G` as being
`List<Graph>`.  (The definition of `Graph` itself is unspecified and outside of
the scope here.)

What representation is actually used for the graph here?
And are there lateral connections displayed between members of G?
That user can pick?

In the centre, there is a graph view -- of an unspecified type, force-directed
or otherwise -- that displays a given element of G.  Initially it displays
nothing: an empty root node.

In the control bar, we have three user-widgets, `Wx`, `Wy`, and `Wz`.

The user starts their session by typing text into `Wx`, which is a free-text
field.  For simplicity we assume there's no auto-complete or help for the user
with this; that's a possible extension.

Once we have the input from `Wx`, we perform a substring match across all elements
of `G`.  This may be slow and may be optimizable, again that's beyond the scope
of this.

This will produce a set of search results: each result is a tuple consisting of
a graph and a node reference within that graph, specified however you like.

These graphs can be rendered across the screen, with the selected node in each
graph 'centred' within each display.

Now, the other columns in the control bar come into play.  The 

Actually, a revision of the data model.  It's always a graph of the whole 
differentiating process, each token narrows the graph.  So for the full data set

id=1: `farmer and cow dealer`
id=2: `a Dutchman`
id=3: `a cow keeper`
id=4: `cow-keeper and carman`

If you search for 'cow', then the following will happen:

1.  `cow` is focused
2.  Links are presented: forward links, in this case `dealer` and `keeper`.
This is one level of forward link.  The target node `keeper` has a greater weight
or priority than `dealer`, because there are two possible job expressions that
are addressed by it.
3.  Once you click through to `keeper`, you then have further options.  The chain
may end here: the user clicks confirm.

There are several questions here around how links work.

1.  Should we be showing reverse links?
2.  Once you followed a chain all the way in, what have you actually done -- eg,
how have you actually helped to generate a taxonomy?
Perhaps the user suggests that this correct pair belongs to this taxonomical group,
which they specify as a hierarchy expression (with a max depth of say 
3.  How does this taxonomy link in to the existing taxonomy proposals being
    addressed by Tim & Ben's Keele project?
4.  How do we want to display the existing selected graph chain?
5.  Once we followed a given chain to its source, what does it actually tell us?
Aside from its position within a taxonomy?

"Cognitive zoom" -- This yet to be specified concept from Alex decides the 
"horizon" -- the number of adjacent graph nodes shown in the visualization at
any given time.

What about the ability to "upvote" and "downvote" edges -- Let's just consider
how does this actually help?

And also the idea that later widgets, i.e. Wz confers a higher 'weight'?  But weight in what sense?

## Note 1

The tokenizer we can refer to as _T_ and it may chunk data in various ways.  It
may also pre-disambiguate certain spellings and misspellings of words: oil,
oyle, etc.  For the purposes of this spec we assume that words are uniquely
designated.  Stemming may also be applied here.

# README (2nd try)

I will try to describe the tool from a UI-first perspective.

In the centre we have a single node; this node represents one word or token.
This node is designated the 'ego node'.
At the top of the interface we show what I call 'breadcrumb', this is the 
path-taken-so-far.

For instance let's take the following data set, represented as JSON

    [
        "surveyor and builder",
        "articled pupil to a surveyor",
        "builder and surveyor",
        "builder, carpenter, and bricklayer",
        "a carpenter and dealer in building materials"
    ]

Note that we've punted on the tokenization things here.

To rephrase Alex's description to me on 22/03, there are actually two different
functions here.

Let's define a phrase here, the *cognitive horizon*.  This basically means the
distance to show radiating nodes.  For instance, imagine that `builder` was
selected as the ego node.

In this case, with a cognitive horizon of 1, the graph would look as such:


    carpenter <--- builder ----> and

Assuming that there's no special handling on 'stop words'.

But with a cognitive horizon of 2, two paths would be shown:

    and <--- carpenter <--- builder ----> and ---> surveyor

These paths are highlightable and saveable in some form.
In addition, through some method (probably a menu item) it would then be possible
to *re-centre* the visualization on a given nodes.


