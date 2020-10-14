# from rauth import OAuth2Service
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope
from twitchAPI.oauth import UserAuthenticator

scope = [AuthScope.CHANNEL_READ_SUBSCRIPTIONS, AuthScope.BITS_READ]
twitch = Twitch(
    "321bx055r6dukooktl98z4bjcc3lxx", "ahuuleft1n1v6lei5onny04vb0kgtn"
)
# twitch.authenticate_app(scope)

auth = UserAuthenticator(twitch, scope)

token, refresh_token = auth.authenticate()

twitch.set_user_authentication(token, scope)


