# Raspberry Pi DHT22 Weather Station Python Flask Socketio  
A DHT Weather Station project using Python, Flask, Flask-SocketIO, and Bootstrap that displays real-time temperature and humidity sensor readings using your Raspberry Pi
  
## Writeup
https://www.donskytech.com/raspberry-pi-dht22-weather-station-project/
sudo apt install python3 python3-venv python3-flask python3-pip  libsystemd-dev pkg-config

python -m venv .venv
source .venv/bin/activate
deactivate
```
3. Install the dependencies
```

pip install -r requirements.txt
cp config_.yaml config.yaml
```

4. Run the application
```
flask run --host=0.0.0.0
```
5. Access the application using the following URL
```
http://127.0.0.1:5000/
```
  
  
### Multiple DHT22 IoT Weather Station Dashboard
This is a follow up project to this project.  It will display dynamic number of DHT22 sensors and its readings.
https://www.donskytech.com/raspberry-pi-weather-station/

Code:  
https://github.com/donskytech/dht22-weather-station-python-flask-socketio-multiple-sensors
  
### How to auto-start this project when your Raspberry Pi boots or starts?  
https://www.donskytech.com/raspberry-pi-how-to-start-python-script-on-boot/
https://plotly.com/javascript/multiple-axes/
https://github.com/plotly/plotly.js/tree/master/dist



sudo cp weather_stantion.service /etc/systemd/system/weather_stantion.service
sudo systemctl daemon-reload

sudo systemctl status weather_stantion.service
sudo systemctl restart weather_stantion.service
sudo systemctl stop weather_stantion.service
sudo systemctl enable weather_stantion.service
journalctl -u weather_stantion.service -f

sshfs olemin@nas.local:/home/olemin/ -p 22 ~/mnt
ssh olemin@nas.local

https://towardsdatascience.com/how-to-add-on-screen-logging-to-your-flask-application-and-deploy-it-on-aws-elastic-beanstalk-aa55907730f
https://plotly.com/javascript/configuration-options/

https://morioh.com/a/96eb0b5d6908/the-easy-way-to-work-with-csv-json-and-xml-in-python
#todo
220 separated mqtt post to 220 powered devices
220 by nearest 2 2 пропущених підняд -= немає живлення

[TinyDB]