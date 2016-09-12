#!/bin/bash

dmesg | grep -i UVD
sudo apt-get remove libcheese-gtk23
sudo apt-get update
sudo apt-get install mesa-vdpau-drivers libvdpau1
sudo apt-get install vdpauinfo
sudo apt-get build-dep mplayer

