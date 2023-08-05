# Raspberry Pi 

Developed for a Pi Zero W, but should work on the others as well. Just make 
sure any kind of internet connectivity is available.

## Install instructions

Install via pip, but be sure to use the 3 version.

```bash
pip3 install raspi_logger
```

The other possibility is to clone the repo to `/home/pi/` and run inside the repo:

```bash
python3 setup.py develop
```



I used a Raspian image for development. 

to describe:

* enable SSH
* enable WiFi
* ~enable W1~
* ~(depending on kernel version, use GPIO4 and GPIO17 for W1)~

### Enable one wire on startup

The script `raspi_logger/enable_w1.sh` enables W1 on GPIO 4 and 17.
Run the script with root privileges on each startup. 
Do that either by hand like:

```sh
sudo chmod 755 raspi_logger/enable_w1.sh
sudo crontab -e
```
And then in the file add the line:
```sh
@reboot path/to/raspi-logger/raspi_logger/enable_w1.sh
```

The CLI of the module can activate the cronjob using the correct paths for you as well.
But you need to run python with `sudo` then and need to install the package for root user 
as well.
Then:

```bash
sudo python3 -m raspi_logger enable_w1
```




