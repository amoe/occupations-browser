import boltkit.controller

realpath = boltkit.controller._install(
    edition='community',
    version='3.4.6',
    path="ext"
)
print("Initialized home at", realpath)
controller = boltkit.controller.create_controller(path=realpath)
controller.start()
print("Started!")
controller.stop()
