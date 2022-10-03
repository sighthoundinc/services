SCRIPT_PATH="`dirname \"$0\"`" 

export SRC_PATH=${SCRIPT_PATH}/../../..
cd ${SRC_PATH}

echo "Building: profile=${CONAN_PROFILE}, SCRIPT_PATH=${SCRIPT_PATH}, ref=${CONAN_REF}"
echo "Env - Begin ======================================================"
env
echo "Env - End ========================================================"

function cleanupConan() {
    conan remove -f ${CONAN_REF}
}

function checkRet() {
    retVal=$1
    msg=$2
    if [ $retVal -ne 0 ]; then
        cleanupConan
        echo $msg
        exit -1
    fi
}

function doUpload() {
    if [ "${LOCAL_SKIP_UPLOAD}" = "true" ]; then
        return
    fi
    ref=$1
    conan upload ${CONAN_OPTIONS_UPLOAD} $ref
    checkRet $?  "conan upload failed for ${ref}"
}

echo "Running in `pwd`"

conan create -pr ${CONAN_PROFILE} conanfile.py $CONAN_REF ${CONAN_OPTIONS_PLATFORM}
checkRet $? "conan create failed for ${CONAN_REF}"
doUpload ${CONAN_REF}

cleanupConan
exit 0