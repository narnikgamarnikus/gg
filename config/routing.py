from channels.routing import route, include
from gg.services.consumers import services_connect, services_disconnect, services_message

services_channel_routing = [
	route("websocket.connect", services_connect),
	route("websocket.receive", services_message),
    route("websocket.disconnect", services_disconnect),
]

channel_routing = [
    include(services_channel_routing, path=r'^/services/'),
]
