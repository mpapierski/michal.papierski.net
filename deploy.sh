#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Hugo version
version="$(hugo version)"

# Build stuff
hugo

# Add changes to git.
git add public/

# Commit changes.
msg="Rebuilding site `date`

hugo version:

    $version
"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"
