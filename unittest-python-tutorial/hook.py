from mamba import description, before, it
from expects import expect, equal, have_length

class Stuff(object):

    def __init__(self):
        self._elements = []

    def elements(self):
        return self._elements

    def add_element(self, element):
        self._elements.append(element)

with description(Stuff) as self:

    with before.each:
        # Initialize a new stuff for every example
        self.stuff = Stuff()

    with it('has 0 elements'):
        expect(self.stuff.elements()).to(have_length(0))

    with it('accepts elements'):
        self.stuff.add_element(object())

        expect(self.stuff.elements()).to(have_length(1))
