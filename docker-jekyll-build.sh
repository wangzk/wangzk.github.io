#!/bin/bash
# Build the site
docker run --rm   --volume="$PWD:/srv/jekyll"   -it jekyll/jekyll:3.8  jekyll build
# Serve the site
docker run --rm   --volume="$PWD:/srv/jekyll"   --publish [::1]:4000:4000   jekyll/jekyll:3.8   jekyll serve