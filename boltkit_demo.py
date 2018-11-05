import boltkit.controller
import boltkit.config

realpath = 'ext/neo4j-community-3.4.6'


realpath = boltkit.controller._install(
    edition='community',
    version='3.4.6',
    path="ext"
)
print("Initialized home at", realpath)
boltkit.config.update(
    realpath,
    {boltkit.config.BOLT_LISTEN_URI_SETTING: 'bolt://127.0.0.1:7687'}
)

controller = boltkit.controller.create_controller(path=realpath)
controller.start()
print("Started!")
controller.stop()

