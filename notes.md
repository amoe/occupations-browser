2018-11-05

"Protocol family unavailable" on travis -- 

I ran into this in the process of setting up travis-ci; within its environments,
ipv6 :: is resolved, but cannot be bound. Fixed by 36c77dd.

Need to re-derive the integration test base case and reform it as neo4j.
