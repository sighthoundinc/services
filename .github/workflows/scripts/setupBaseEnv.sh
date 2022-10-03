export CONAN_PROJ=`cat version.properties | grep name | sed 's/name=//g'`
export CONAN_VER=`cat version.properties | grep version | sed 's/version=//g'`
export CONAN_BRANCH=`echo ${GITHUB_REF} | sed s~^refs/heads/~~g | sed s~^refs/pull/~~g | sed s~/~_~g`
if [ "${CONAN_BRANCH}" != "master" ]; then export CONAN_BRANCH=branch_${CONAN_BRANCH}; fi
export CONAN_REF=$CONAN_PROJ/$CONAN_VER@sighthound/${CONAN_BRANCH}
export CONAN_OPTIONS_UPLOAD=" --force -r sighthound --all --confirm --parallel "

# We assume runner home folder is in the homedir.
# /home/ubuntu/actions-runner/workspace/Platform/Platform
export GITHUB_RUNNER_NAME=`echo ${GITHUB_WORKSPACE} | cut -d/ -f4 | cut -d- -f2`

echo "CONAN_BRANCH=${CONAN_BRANCH}" >> $GITHUB_ENV
echo "CONAN_REF=${CONAN_REF}" >> $GITHUB_ENV
echo "CONAN_VER=${CONAN_VER}" >> $GITHUB_ENV
echo "CONAN_OPTIONS_UPLOAD=${CONAN_OPTIONS_UPLOAD}" >> $GITHUB_ENV
echo "GITHUB_RUNNER_NAME=${GITHUB_RUNNER_NAME}" >> $GITHUB_ENV

echo "Building ${CONAN_REF}"