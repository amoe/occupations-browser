import {assert} from 'chai';
import mymodule from '../src/mymodule';

it('trivially uses typescript', function() {
    assert.isTrue(true);
});

it('can call function from another module', function() {
    assert.equal(mymodule.meaningOfLife(), 42);
});
