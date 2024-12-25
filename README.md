
# Installing updated firmware

You will need:
- 1x micro-USB cable
- 1x light jar (duh)
- 1x firmware file

## To get the firmware file

First download the files from github. This can be done by clicking on the `compiled_fw` folder, then the `firmware.uf2` file, then select 'View raw'. The file should download. If it does not, you can click the little download icon to the left above the 'View raw' text.

# To update the light jar microcontroller

Disconnect the power and take the light jar apart and slide the top cap free of the helical light structure. A green microcontroller board with a small raspberry logo should be visible. On the top of this green board, a small white button near a micro-USB socket will be at the 'bottom' of it. 

While depressing the white button, plug the micro-USB cable into the microcontroller. It should show up on your computer as a USB drive named `RPI-RP2`.

Drag and drop the `firmware.uf2` to copy it into the `RPI-RP2` drive.

The device should disconnect, showing the firmware is correctly written! A small LED should start flashing on the light jar to indicate it is functioning.

# Compiling to UF2 binary
Get things setup and ready
```
sudo apt install git gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential cmake

git clone git@github.com:micropython/micropython.git

cd micropython/mpy-cross
make

cd ../

git submodule update --init lib/pico-sdk lib/tinyusb
```
Then copy the necessary files into the `ports/rp2/modules` directory. 

To get picotool working right, I git cloned it and set a system variable to point to its location.
`export PICOTOOL_FETCH_FROM_GIT_PATH=~/gitrepos`
I also compiled it, which involved a pretty typical cmake build sequence instructions on picotool website.

I did run into a compiler dependency issue, where I needed the libstdc++ package.
`sudo apt install libstdc++-arm-none-eabi-newlib`

I was then able to finally compile it...
```
cd ports/rp2

make
```
The output files should be within the `ports/rp2/build-PICO` directory.
