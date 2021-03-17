# sentinel3-altimetry-l2
Toolbox for sentinel-3 altimetry level2 product processing
## 1. Introduction
This repository is built for the radar/sar altimetry data processing. this repository contains folders as follows:
1) ipynb: test code for the basic functions built in this repo.
2) results: processing results by the .ipynb file.
3) test_data: contains data tested in the repo, such as altimetry data, tide gauge data, and satellite image. (note: this dir not be uploaded due to large size)
4) utils: .py file corresponding to the processing functions built in this repo.
## 2. Features
1) we construct a 1d-cnn (1 dimentional convolutional neural network) model for the ocean-like waveform recognition.
2) we use ransac algorithm for the ssha values prediction.


