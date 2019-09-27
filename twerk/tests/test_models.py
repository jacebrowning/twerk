# pylint: disable=unused-argument,unused-variable,expression-not-assigned,no-member


from ..models import Bot


def describe_bot():
    def describe_init():
        def it_defaults_to_now_for_joined(expect):
            bot = Bot("foobar")
            expect(bot.datafile.data) == {
                "tweets": 0,
                "following": 0,
                "followers": 0,
                "joined": "March 2006",
            }
