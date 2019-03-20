#! /bin/sh

echo "Posting query..."
result=$(cat query.json | http -h --pretty=none post http://localhost:5000/micromacro-query)
redirect=$(printf "%s\n" "$result" | tr -d '\r' | sed -n 's|^Location: ||p')
echo "Getting query result..."
http -b get "$redirect"
