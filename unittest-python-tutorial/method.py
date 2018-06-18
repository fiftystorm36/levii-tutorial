from mamba import description, context, it

with description('Refactoring Goodies') as self:
    with it('allows calling a defined method inside the example group'):
        assert self.hello('python') != self.hello('pandas')

    def hello(self, world):
        return 'hello, %s'.format(world)
