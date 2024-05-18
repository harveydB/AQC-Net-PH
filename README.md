# AQC Net PH

This project utilizes image-based air quality monitoring through deep learning using low-cost particulate matter sensors. 

## Dependencies
Running the following command will install the prerequesites needed

This model uses a deep convolutional neural network model AQC-Net based on ResNet in addition to the addition of the self supervision model SCA that estimates air pollution by using both PM2.5 and PM10 concentration levels. 

![image](https://github.com/harveydB/AQC-Net-PH/assets/80321695/ea242e04-d3c6-43b2-9767-533a3db6f8d3)



```
pip install -r requirements.txt
```

```
title: AQC Net PH Space
emoji: ⚡
colorFrom: green
colorTo: red
sdk: gradio
sdk_version: 2.9.4
app_file: app.py
pinned: false
license: apache-2.0
```
---

Try using this application at https://huggingface.co/spaces/jervinjosh68/AQC-Net-PH-space

Check out the configuration reference at https://huggingface.co/docs/hub/spaces#reference
