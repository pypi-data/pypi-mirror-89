
from collections import defaultdict



class Subscription:

    def __init__( self, bus, topic, handler ):
        self.bus = bus
        self.topic = topic
        self.handler = handler


    def unsubscribe( self ):
        self.bus.subscriptions[self.topic].remove( self )



class MessageBus:

    def __init__( self ):
        self.subscriptions = defaultdict( list )


    def publish( self, topic, *args, **kwargs ):
        for subscription in self.subscriptions[topic]:
            subscription.handler( *args, **kwargs )


    def subscribe( self, topic, handler ):
        subscription = Subscription( self, topic, handler )
        self.subscriptions[topic].append( subscription )
        return subscription

