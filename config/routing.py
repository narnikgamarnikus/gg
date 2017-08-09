from channels.routing import route, include
from gg.services.consumers import bet_connect, bet_disconnect

bets_channel_routing = [
    route("websocket.connect", bet_connect),
    route("websocket.disconnect", bet_disconnect)
]

#channel_routing = [
#    include(bets_channel_routing, path=r'^/bet/'),
#]

channel_routing = [
    route("websocket.connect", bet_connect),
    route("websocket.disconnect", bet_disconnect)
]
