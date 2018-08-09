# main.mk

# This makefile will create a buildable distribution under the 'dist' directory
# that can be deployed to a server.

WEBPACK = ./node_modules/.bin/webpack
dist_path = dist

dist: dist/bundle.js
	mkdir -p dist
	cp -a index.html static $(dist_path)

.PHONY: dist

dist/bundle.js: src
	$(WEBPACK)
