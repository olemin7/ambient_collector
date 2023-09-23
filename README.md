# Raspberry Pi DHT22 Weather Station Python Flask Socketio  
A DHT Weather Station project using Python, Flask, Flask-SocketIO, and Bootstrap that displays real-time temperature and humidity sensor readings using your Raspberry Pi
  
## Writeup
https://www.donskytech.com/raspberry-pi-dht22-weather-station-project/

python -m venv .venv
source .venv/bin/activate
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


sudo cp weather_stantion.service /etc/systemd/system/weather_stantion.service
sudo systemctl daemon-reload

sudo systemctl status weather_stantion.service
sudo systemctl restart weather_stantion.service
sudo systemctl stop weather_stantion.service
sudo systemctl enable weather_stantion.service
journalctl -u weather_stantion.service -f

sshfs olemin@central.local:/home/olemin/ -p 22 ~/mnt
ssh olemin@central.local