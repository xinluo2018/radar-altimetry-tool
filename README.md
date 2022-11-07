# sentinel3-altimetry-l2
Toolbox for sentinel-3 altimetry level2 product processing
## 1. Introduction
This repository is built for the radar/sar altimetry data processing. this repository contains folders as follows:
1) notebook: basic workflow for main processing.
2) utils: .py file corresponding to the processing functions built in this repo.
## 2. Data
Download from: https://scihub.copernicus.eu/dhus/#/home

## 3. Features
1) we construct a 1d-cnn (1 dimentional convolutional neural network) model for the ocean-like waveform recognition.
2) we use ransac algorithm for the elevation values filterd and prediction.

## Todo
1) complete the cryosat-2 data read and write out.
2） cryosat, jason-3 data processing.
3) modify the utils/elev_cal_s3l2-modify.py, make this script can calculate the inland water height correctly (current is the sea surface height anomaly calculation).
