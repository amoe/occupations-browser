So my question is -- and don't kill me -- what should the fold/unfold behaviour
actually be?

What I've previously called 'widget-groups' in our last conversation, I've now
renamed as 'compound widgets'.  The individual selectors of taxons I'm thinking
about renaming to taxon-selectors, logically enough...

So I remember that I did the animation that's shown on the 'About' page of the
demo site to try to demonstrate how this fold / unfold behaviour would operate.

However, what's the detailed definition of this behaviour, what should happen
under which circumstances?


Alex [10:14 AM]
Gee, thanks for that question :slightly_smiling_face:

Let’s try walking through the UX from the point at which you have just created a
taxon-selector (TS from hereon). (edited) At this point, you have to select a
taxon: taxonomy first. That will then cause (a) the ‘create next level TS’
button (the square in circle on the TS) to darken to black - assuming that there
is a ‘next level’ for the taxonomy in question (since we’ve just started, there
should be!), (b) a filled red circle to appear on the TS, indicating that this
is now the active, top level TS for a ‘compound widget’-in-potential but
currently with only a single-TS, (c) the ‘next level TS create’ button on this
TS to become greyed-out again. (edited) On clicking the ‘create next level TS’
button, a second TS will slide out taking it’s place to the right of the initial
TS

This second TS can then be configured, with the available Taxon-selector field
offering one level down from that selected in the TS to its left. When a
selection is made (a) the _single_ filled red button on TS1 becomes two red
buttons, both filled (because both of the available TSs are visible, and this TS
is the top level), (b) two red buttons appear on TS2, the left empty, the second
filled (because there are now two TSs, of which this is the second and visible),
(b) If there is another available taxon level below that set in TS2, then the
‘create next level TS’ button in TS2 turns black.  etc for the creation of
additional TSs

‘Retracting/Collapsing TSs’ … (edited)

The red buttons are the mechanism used to retract/collapse/expand and foreground TSs

A sequence of red buttons (whether outline or filled) represents the currently active TSs in any ‘compound widget’.

On any individual TS they are filled to indicate both (a) the place in the TS
hierarchy of that TS, (b) any TSs below it in the hierarchy that are also
visible. (edited)

The red filled/outline buttons then operate to select which of the TSs in a
‘compound widget’ are visible, as follows:

Alex [10:49 AM]
The effect of clicking a _filled_ red button depends on whether the button clicked refers to the TS on which it appears (ie. if its the middle of three TSs, is it the middle button of three)

If it is the TS-self-button, any other TSs slide under that button to leave it
as the only TS visible

If it is _not_ the TS-self-button, any TSs to the right of the TS that is
referenced slide under that button. (edited)

Whenever a TS becomes _non-visible_, its representative button on any other TS
becomes ‘outline’ - _with_ a red dot in its centre [NOTE: the red dot in the
centre is a new introduction!] (edited)

Clicking any red outline-with-dot circle causes that TS only to slide out (to
right or left of - or between - the current TS/s) to take its correct place in
the ‘compound widget’ sequence. Button glyphs change to reflect the change in
visibility.

OK, SO I CONFESS THAT THIS IS ME THINKING THROUGH ON MY FEET - EXTEMPORISING - SOMETHING I HADN’T PREVIOUSLY WORKED THROUGH SUFFICIENTLY!

Hence the introduction of the ‘outline button with red dot’ - so that red
buttons now have three states: outline (it’s visible but not the TS on which the
button site), filled (it’s the TS on which the button sits, or a TS higher in
the hierarchy), outline-with-dot (it exists but is current non-visible)

Doubtless there are flaws in my logic here. I’ll think it through again but let
me know if/when you spot one!  IMMEDIATELY - on reflection - I’M THINKING THAT
THIS IS ALL TOO COMPLICATED. THERE MUST BE A SIMPLER SOLUTION. GIVE ME A FEW
MINUTES …

Alex [11:18 AM]

Ok, an alternative, much simpler way of thinking about the red buttons and
un/fold behaviour. Tell me what you think of this

The buttons simply represent the visible/invisible state of any TS in the
sequence, and are used to toggle between these.

TSs that are higher in the hierarchy slide out to the left (displacing the
current TS/widget-group by one place to the right), TSs that are lower slide out
to the right (displacing subsequent TSs from different widget-groups, to the
right), TSs that are between other currently visible TSs in a widget group,
insert themselves into the visible group, pushing any TSs lower in the hierarchy
to the right to make space.

In reverse, any TS made invisible either (a) causes any TSs to its right to
slide left over it, shifting everything to the left, or (b) if it is the lower
taxon level currently visible, it slides under the next TS to its left (in the
widget group), drawing any other TSs widgets to its right with it.

When only one TS in a widget-group is ‘on’ - it cannot be turned off (maybe its
filled red dot becomes a darker shade?)  DONE
