# Разработка платформы OpenAR
**_Внимание, раздел не дописан!_**

## Сборка и запуск APK
```shell
git clone https://github.com/usiqwerty/openar.git
cd openar
```
```shell
sudo apt-get update
sudo apt-get install -y curl
sudo apt-get install -y python3-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
```


```shell
sudo apt-get install -y \
    	python3-pip \
    	build-essential \
    	git \
    	python3 \
    	python3-dev \
    	ffmpeg \
    	libsdl2-dev \
    	libsdl2-image-dev \
    	libsdl2-mixer-dev \
    	libsdl2-ttf-dev \
    	libportmidi-dev \
    	libswscale-dev \
    	libavformat-dev \
    	libavcodec-dev \
    	zlib1g-dev
```

```shell
# Dependencies Kivy
sudo pip3 install cython

# Install Kivy
sudo pip3 install kivy
```
```shell
wget http://mirrors.kernel.org/ubuntu/pool/main/libi/libidn/libidn11_1.33-2.2ubuntu2_amd64.deb
sudo apt install ./libidn11_1.33-2.2ubuntu2_amd64.deb
```
```shell
sudo apt install -y \
    	build-essential \
    	ccache \
    	git \
    	libncurses5 \
    	libstdc++6 \
    	libgtk2.0-0 \
    	libpangoxft-1.0-0 \
    	libidn11 \
    	python3 \
    	python3-dev \
    	openjdk-17-jdk \
    	unzip \
    	zlib1g-dev \
    	zlib1g \
    	libltdl-dev \
    	libffi-dev \
    	libssl-dev \
    	autoconf \
    	autotools-dev \
    	cmake
#libpangox-1.0-0 \
```
```shell
# Install Buildozer
pip install git+https://github.com/kivy/buildozer.git
```

```shell
echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list 
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add - 
sudo apt-get update 
sudo apt-get install bazel
```
https://raw.githubusercontent.com/HeaTTheatR/KivyMD-data/master/install-kivy-buildozer-dependencies.sh

```shell
buildozer android debug
```