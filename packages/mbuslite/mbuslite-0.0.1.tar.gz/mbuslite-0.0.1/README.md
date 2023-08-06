
# mbuslite

`mbuslite` provides a message bus implementation embedded within the application's process.

With it, you can loosely couple your application components. It implements the publish-subscribe
pattern.

## Motivation

Having worked with crossbar and autobahn, as well as DBus, I like the message bus pattern. I've
wanted to use it in some projects to achieve the same loose coupling between internal components.

Having also worked wih sqlite, I like the simplicity of a library instead of a remote service.

Thus, `mbuslite`.

