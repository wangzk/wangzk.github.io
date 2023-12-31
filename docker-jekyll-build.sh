#!/bin/bash
# Build the site
podman run --rm   --volume="$PWD:/srv/jekyll"   -it docker.io/jekyll/jekyll:3.8  jekyll build
# Serve the site
#podman run --rm   --volume="$PWD:/srv/jekyll"   --publish [::1]:4000:4000   docker.io/jekyll/jekyll:3.8   jekyll serve
