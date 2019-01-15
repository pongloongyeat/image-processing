# Image processing codes for my university's summer project Y18/19.

Image processing codes for a robot that navigates the blind. The codes here work to read signs and extract text and directional (arrow) data in order to guide the blind around.

## Getting started

To get started, clone a copy of this project onto your working environment. Then, download the required prerequisites.

### Prerequisites
* [Python 2.7.9 and above](https://www.python.org/downloads/) - 2.7.9 and above
* [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) - 4.0.x (Windows)

### Installation (Windows)

Download and install [Python 2.7.9 and above](https://www.python.org/downloads/) (not Python 3) and a simple IDE such as [PyCharm](https://www.jetbrains.com/pycharm/) or any equivelant IDE. 

Open the project folder as a PyCharm project (or with your equivelant IDE) and make sure Python 2.7 is selected as the Project Interpreter. Then, install the following packages.
```
numpy
imutils
opencv-python (v3.4.5.20)
```
Install (Tesseract-OCR)[https://github.com/tesseract-ocr/tesseract/wiki] (follow the instructions for Windows). 

Copy the installation directory for Tesseract (usually `C:\Program Files (x86)\Tesseract-OCR`) and add the installation directory as a `PATH` variable.

Finally, install the `pytesseract` package and you're set.

### Installation (Raspbian)

Check and ensure Python and Pip is installed on your Raspbian OS (should be pre-installed by default) If using a used Raspberry Pi (that we may have worked on), check if OpenCV 3.4.5.x is already installed by opening up the terminal and entering the following:
```
python
import cv2
cv2.__version__
```
If there are no errors and it returns a version later than `3.4.5`, then OpenCV 3.4.5 is already installed on your Pi and you make skip the OpenCV installation steps.

Otherwise, open up the terminal and enter the following:
```
sudo pip install --upgrade pip
sudo pip install numpy
sudo pip install imutils
sudo pip install pytesseract
```
Then, head over to the [OpenCV SourceForge page](https://sourceforge.net/projects/opencvlibrary/files/3.4.5/) and save and extract the  `OpenCV 3.4.5.zip` file to `/home/pi/`.

Rename the extracted folder to `opencv-3.4.5`. Open up the terminal again and enter the following:
```
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
```
Once all the required libraries are installed, we can now setup our OpenCV build using CMake:
```
cd opencv-3.4.5
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_PYTHON_EXAMPLES=ON -D WITH_FFMPEG=OFF -D INSTALL_C_EXAMPLES=ON -D BUILD_EXAMPLES=ON ..
```
If all goes well without any errors, we can now compile OpenCV (Takes about 2 hours to compile):
```
make -j4
```
Once that is done, we can now install OpenCV:
```
sudo make install
```
And we're done!

## Contributors

* Pong Loong Yeat
* Calvin Low Fu Yuan
* Claire Jewel Wong Mae Mae
