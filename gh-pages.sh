#!/bin/bash

set -o errexit; set -o nounset; set -o pipefail

pushd `dirname $0` > /dev/null
SCRIPT_PATH=`pwd`
popd > /dev/null

BASE_PATH="$(dirname "${SCRIPT_PATH}")"

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[1;32m'
NC='\033[0m' # No Color

html_docs=${SCRIPT_PATH}/docs/_build/html
remote_url=$(git config --get remote.origin.url)
commit_message="Updating gh-pages docs"

if ! git ls-remote --exit-code --heads ${remote_url} gh-pages 2>&1; then
	printf "${RED}Unable to find gh-pages branch in repository ${remote_url}${NC}\n"; echo

	printf "${RED}Before building docs you have to create orphaned gh-pages branch in the repo ${remote_url}${NC}\n"; echo
	printf "\tStep 1: git checkout --orphan gh-pages\n"
	printf "\tStep 2: git rm -rf .\n"
	printf "\tStep 3: echo \"Initial gh-pages page\" > index.html\n"
	printf "\tStep 4: git add index.html && git commit -m \"Initial commit gh-pages\" && git push origin gh-pages\n"; echo
	exit 2
fi

tmp_clone_location=$(mktemp -d 2>/dev/null || mktemp -d -t 'gh-pages')

cd "${html_docs}"
git clone ${remote_url} "${tmp_clone_location}"
cd "${tmp_clone_location}" && git checkout gh-pages

cp -r "${html_docs}/" "${tmp_clone_location}"

git add -A && git commit -m "${commit_message}"
git push origin gh-pages

rm -fr "${tmp_clone_location}"

exit 0
