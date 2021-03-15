# Server
## 1.Remote login server（Linux system）
ssh login：`ssh -i local_dir/nbiot.pem ubuntu@18.162.148.127`\
eg.ssh -i ~/Downloads/nbiot.pem ubuntu@18.162.148.127
## 2.Running the listener script
* cd listener
* python3 test.py
# Client（sensor_v01）
## 1.Program the files in folder TCP_sensor_v01/source into the MCU based on MCUXpressoIDE
## 2.Running program，choose mode 5
## 3.Press the GNSS-RESET button on sensor_v01 according to the prompt 

