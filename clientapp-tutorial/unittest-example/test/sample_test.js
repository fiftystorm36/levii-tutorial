//var assert = require('power-assert');
import assert from 'power-assert'
import Cat from '../src/cat'

describe('Cat', () => {
    var tama;
    beforeEach(() => {
        tama = new Cat('tama')
    });

    describe("greet()", () => {
        it("挨拶をする", () => {
            assert.equal(tama.greet(), 'Nyaaaan! I am neko');
        });
    });
});

describe('Array', function () {
    describe('#indexOf()', function () {
        it('should return -1 when the value is not present', function () {
            assert.equal(-1, [1, 2, 3].indexOf(5));
            assert.equal(-1, [1, 2, 3].indexOf(2));
        });
    });
});
