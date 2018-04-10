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


