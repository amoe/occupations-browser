import occubrow.system

backend = occubrow.system.get_backend()
result = backend.search_tokens('ee')
print(result)

backend = occubrow.system.get_backend()
result = backend.get_all_tokens()
print(result)

