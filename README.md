# AQC Net PH

This project utilizes image-based air quality monitoring through deep learning using low-cost particulate matter sensors. 

___________________________________________________________________________________________________________________________________________________________________________________________________________________

## Dependencies
Running the following command will install the prerequesites needed

```
pip install -r requirements.txt
```

---
title: AQC Net PH Space
emoji: ⚡
colorFrom: green
colorTo: red
sdk: gradio
sdk_version: 2.9.4
app_file: app.py
pinned: false
license: apache-2.0
---

Try using this application at https://huggingface.co/spaces/jervinjosh68/AQC-Net-PH-space

Check out the configuration reference at https://huggingface.co/docs/hub/spaces#reference

The training model for this project uses a deep convolutional neural network model AQC-Net based on ResNet in addition to the addition of the self supervision model SCA that estimates air pollution by using both PM2.5 and PM10 concentration levels. 

![image](https://github.com/harveydB/AQC-Net-PH/assets/80321695/ea242e04-d3c6-43b2-9767-533a3db6f8d3)

The Spatial and Context Attention Block (SCA) created by Zhang et al.(2020)  is introduced at the 3rd Block in the ResNet18 network structure. The SCA module is used to recalibrate the feature mapping of the channels and its basic structure is composed of two parts

The first part of the SCA is used to encode the wider scene context information into local features, tocalculate the correlation between the channels, and to enhance the representation ability of the module. 

The second part is used to aggregate the spatial context information that improves the specific scene informationof each channel and adjust the interdependence of the channels accurately. The introduction of the SCA block will increase the classification accuracy compared to the standalone ResNet18.


![image](https://github.com/harveydB/AQC-Net-PH/assets/80321695/e42c497b-2d58-4166-a2b4-28719934631e)





