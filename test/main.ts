import chai, { assert } from 'chai';
import mymodule from '../src/mymodule';
import graph from '../src/graph';

chai.config.truncateThreshold = 0;

it('trivially uses typescript', function() {
    assert.isTrue(true);
});

it('can call function from another module', function() {
    assert.equal(mymodule.meaningOfLife(), 42);
});


const singleItemChain = ["in", "the", "brandy"];
const singleItemGraph = {
    token: "in",
    children: [
        {
            token: "the",
            children: [
                {
                    token: "brandy"
                }
            ]
        }
    ]
};

it('can be transformed to a graph', function() {
    const result = graph.stratifySentence(singleItemChain);
    console.log("result was %o", JSON.stringify(result));

    assert.deepEqual(
        result,
        singleItemGraph
    );
});

