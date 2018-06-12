from mamba import description, context, it
from expects import expect, equal

#import tennis

# executed by 'mamba filter.py -t integration'
with description('Tennis1', 'integration') as self:
    with it('starts with 0 - 0 score'):
        rafa_nadal = "Rafa Nadal"
        roger_federer = "Roger Federer"
        game = tennis.Game(rafa_nadal, roger_federer)

        expect(game.score()).to(equal((0, 0)))

# executed by 'mamba filter.py -t unit'
with description('Tennis2', 'unit') as self:
    with it('starts with 0 - 0 score'):
        rafa_nadal = "Rafa Nadal"
        roger_federer = "Roger Federer"
        game = tennis.Game(rafa_nadal, roger_federer)

        expect(game.score()).to(equal((0, 0)))
