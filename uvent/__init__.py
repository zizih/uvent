# coding=utf8

# Copyright (C) 2012 Saúl Ibarra Corretgé <saghul@gmail.com>
#

__all__ = ['install']


# Patchers

def patch_sleep():
    import gevent
    def sleep(seconds=0, ref=True):
        hub = gevent.hub.get_hub()
        loop = hub.loop
        watcher = loop.timer(max(seconds, 0), ref=ref)
        hub.wait(watcher)
    gevent.sleep = sleep
    gevent.hub.sleep = sleep

def patch_loop():
    from .loop import UVLoop
    from gevent.hub import Hub
    Hub.loop_class = UVLoop

def patch_dns(use_custom_resolver):
    from gevent.hub import Hub
    if use_custom_resolver:
        from .resolver import Resolver
    else:
        from gevent.resolver_thread import Resolver
    Hub.resolver_class = Resolver


def install(dns=True):
    patch_sleep()
    patch_loop()
    patch_dns(dns)
