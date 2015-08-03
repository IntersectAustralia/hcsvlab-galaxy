#!/bin/bash
sudo apt-get install python-tk -y
sudo apt-get install xvfb -y
sudo apt-get install imagemagick -y
export DISPLAY=:1
Xvfb :1 -screen 0 1024x768x24 &
sudo xhost +
sudo echo "export DISPLAY=:1" >> ~/.bashrc