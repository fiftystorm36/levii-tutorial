from mamba import description, _it

with description('Pending Examples') as self:
    with _it('will not run any pending example (marked with an underscore)'):
        assert False
