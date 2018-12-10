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

function usage() {
    echo "Usage: $0 [option...]" >&1
    echo >&1
    echo "   -v  tag version (1.0.0, 1.2.3, etc)" >&1
    echo "   -y  confirm every input with yes and leave default values intact" >&1
    echo
    echo >&1
}

function git_dirty {
    [[ $(git diff --shortstat 2> /dev/null | tail -n1) != "" ]] && echo "yes" || echo "no"
}

function git_num_untracked_files {
    echo $(git status --porcelain 2>/dev/null | grep "^??" | wc -l)
}

# Reset in case getopts has been used.
OPTIND=1

YES=0
VERSION=""

while getopts "h?v:" opt; do
    case "${opt}" in
    h|\?)
        usage
        exit 0
        ;;
    y)  YES=1
        ;;
    v) VERSION=${OPTARG}
        ;;
    esac
done
shift $((OPTIND-1))
[[ $# -gt 0 && "$1" == "--" ]] && shift
leftover_path="$@"

# Before we do anything let's make sure our working copy is clean.
if [[ $(git_dirty) == "yes" || $(git_num_untracked_files) != "0" ]]; then
    echo; printf "${RED}Error:${NC} You have untracked files in your working copy. Unable to create new release\n"; echo
    exit 1
fi

AWK_VERSION_BUMP=$(cat <<'EOF'
NF == 1 {
    print ++$NF
};
NF > 1 {
    if (index($NF, "-") != 0) {
        last = substr($NF, length($NF));
        if (last ~ /^[0-9]+$/) {
            last += 1;
            stop = length($NF) - length(last);
        } else {
            last = 1;
            stop = length($NF);
        }
        $NF = sprintf("%s%d", substr($NF, 1, stop), last);
    } else {
        if (length($NF + 1) > length($NF))
            $(NF-1)++;
        $NF = sprintf("%-*d", length($NF), ($NF + 1) % (10 ^ length($NF)));
    }
    print
}
EOF
)

current_version=""
if git describe --abbrev=0 --tags > /dev/null 2>&1; then
    current_version=$(git describe --abbrev=0 --tags)
fi
if [[ -z "${VERSION}" ]]; then
    if [[ ! -z ${current_version} ]]; then
        VERSION=$(echo "${current_version//v/}" | awk -F. -v OFS=. "${AWK_VERSION_BUMP}")
    else
        VERSION="1.0.0"
    fi
else
    [[ "${VERSION}" != v* ]] && VERSION="${VERSION}"
fi

master_branch="master"
release_branch="release-${VERSION//v/}"

# Create tag and push changes to master
update_version_files=0
while true; do
    if [[ ${YES} == 1 ]]; then
        YESNO=y
    else
        echo; printf "${YELLOW}Warning:${NC}"
        read -p " Update version to ${VERSION}. Do you want to proceed? (yes/no):" YESNO
    fi
    case ${YESNO} in
        [Yy]*)
        update_version_files=1
        break;;
        [Nn]*)
        break;;
        *)
        echo "Please answer with yes or no";;
    esac
done

if [[ ${update_version_files} == 1 ]]; then
    git checkout -b ${release_branch} ${master_branch}

    # Update version.py
    version_file="${SCRIPT_PATH}/vivialconnect/version.py"
    if [[ -e "${version_file}" ]]; then
        sed -i.backup -E "s,\=.*,\= \"${VERSION}\"," "${version_file}"
        rm "${version_file}.backup"
    else
        echo "version=${VERSION}" > "${version_file}"
        git add "${version_file}"
    fi

    # Update package VERSION
    version_file="${SCRIPT_PATH}/VERSION"
    if [[ -e "${version_file}" ]]; then
        mv "${version_file}" "${version_file}.backup"
        echo "${VERSION}" > "${version_file}"
        rm "${version_file}.backup"
    else
        echo "${VERSION}" > "${version_file}"
        git add "${version_file}"
    fi

    git commit -am "Incrementing version number to ${VERSION}"

    # Merge release branch into master
    git checkout ${master_branch}
    git merge --no-ff ${release_branch} -m "Merged version.py changes for the release version ${VERSION}."

    # Create tag and push changes to master
    confirm_release_push=0
    while true; do
        if [[ ${YES} == 1 ]]; then
            YESNO=y
        else
            echo; printf "${YELLOW}Warning:${NC}"
            read -p " You are about to push version ${VERSION} to the origin server. Do you want to proceed? (yes/no):" YESNO
        fi
        case ${YESNO} in
            [Yy]*)
            confirm_release_push=1
            break;;
            [Nn]*)
            break;;
            *)
            echo "Please answer with yes or no";;
        esac
    done

    if [[ ${confirm_release_push} == 1 ]]; then
        git push origin ${master_branch}
        git tag -a "${VERSION}" -m "Created release ${VERSION}"
        git push --tags
    else
        echo; printf "${YELLOW}Warning:${NC} Relese aborted. You should undo latest commit with the ${GREEN}git reset --hard HEAD~1${NC} command\n"; echo
    fi
    echo; printf "${GREEN}Info:${NC} Removing temp release branch ${release_branch}\n"; echo
    git branch -d ${release_branch}
else
    echo; printf "${YELLOW}Warning:${NC} Relese action canceled\n"; echo
fi
