#!/bin/bash
echo 'Running AMD GPU MM/Gfx Testcases'
SRC_DIR=/mnt/QA_PERFLAB/VDK_Testing/AXELL/Axell_streams/Basic/
DEST_DIR=/home/jenkinshas/Streams/
if [ -d "$DEST_DIR" ]; then
    echo "Removing existing streams folder"
	echo 'amd@123' | sudo -S rm -rf /home/jenkinshas/Streams/
fi

echo 'amd@123' | sudo -S mkdir -p "$DEST_DIR"
echo 'amd@123' | sudo -S chown -R jenkinshas:jenkinshas "$DEST_DIR"
echo 'amd@123' | sudo cp -R $SRC_DIR/* "$DEST_DIR"
echo "Copying New streams"
echo 'amd@123' | sudo cp -R /mnt/QA_PERFLAB/VDK_Testing/AXELL/Axell_streams/MPV_Streams/* "$DEST_DIR"
if [ "$#" == "3" ]; then
	sdkInstallation="no"
elif [ "$#" == "4" ] && [ "$4" == "no" ]; then
	echo "I am here"
	sdkInstallation="$4"
	sdkInstaller="buildRoom"
elif [ "$#" == "5" ] && [ "$4" == "yes" ]; then
	echo "Sdk installation through path mentioned"
	sdkInstallation="$4"
	sdkInstaller="$5"
elif [ "$#" == "4" ] && [ "$4" == "yes" ]; then
	echo "Sdk installation through buildroom"
	sdkInstallation="$4"
	sdkInstaller="buildRoom"	
fi
#./amdgpu_mmgfx_qa_controller.py SQA QA_EG_AXELL_TC 635-639
if [ "$sdkInstallation" == "yes" ]; then
	echo "Installing SDK....."
	./sdkInstallation.py $sdkInstaller
fi

#./sdkInstallation.py "/mnt/QA_PERFLAB/VDK/EG/Pachinko_SDK/2016-05-20-1.0-Beta/Pachinko_Solution/SDK-installer/AMD_PachinkoGaming_sdk_setup-1.0.46.68-Beta.sh"
#echo "Installation done"
var=`grep -inR "AMDPACHINKOSDKROOT" $HOME/.bashrc`
if [ "$var" != "" ]; then
    echo "Exporting AMDPACHINKOSDKROOT variable.. This is workaround"
    envVar=`grep -inR "AMDPACHINKOSDKROOT" $HOME/.bashrc | cut -d "=" -f 2 | cut -d '"' -f 2`
    ldLibraryPath=`grep -inR "LD_LIBRARY_PATH" $HOME/.bashrc | cut -d "=" -f 2 | cut -d '"' -f 2`
    export AMDPACHINKOSDKROOT=$envVar
	export LIBVA_DRIVER_NAME="gallium"
    echo "PACHINKOSDKROOT is set:$AMDPACHINKOSDKROOT"
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ldLibraryPath
    echo "LD_LIBRARY_PATH is set:$LD_LIBRARY_PATH"
fi
./amdgpu_mmgfx_qa_controller.py $1 $2 $3
