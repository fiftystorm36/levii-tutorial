from mamba import description, _context, it

with description('Pending Examples') as self:
    with _context('when running a pending context (marked with an underscore)'):
      with it('will not run any example under a pending context'):
        assert False

      with it('will not be run either'):
        assert False
