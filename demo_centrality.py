import occubrow.system

backend = occubrow.system.get_backend()
r = backend.get_centrality_statistics()
print(r)
