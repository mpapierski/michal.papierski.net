#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Hugo version
version="$(hugo version)"

# Build stuff
hugo

pushd public
# Add changes to git.
git add .

# Save date
when="$(date)"

# Commit changes.
msg="Rebuilding site $when

hugo version:

    $version
"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# Save committed SHA1
committed="$(git rev-parse HEAD)"

git push origin master

popd

git commit -am "Update tracked site artifacts.

Build date:

    $when

hugo version:

    $version

Git SHA1:

    $committed
"
