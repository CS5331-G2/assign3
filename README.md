# bleh

## Mac OS
1. Install ansible using the below command
`brew install ansible`
2. Install Vagrant & VirtualBox
3. Install this vagrant plugin
   `vagrant plugin install vagrant-vbguest`

## Ubuntu
1. Install ansible using the below command
`sudo apt-get install python-pip`
`sudo pip install ansible`
2. Install VirtualBox
`sudo apt-get install virtualbox`
3. [Download Vagrant](https://www.vagrantup.com/downloads.html), and install the x86/x64 debian package of your choice.
4. Install this vagrant plugin
   `vagrant plugin install vagrant-vbguest`

## Next Steps

1. Open the `Vagrantfile` in /Vagrantfile and change syncfile source to the root of this repo.folder. Remember to save the file after that.
2. Type the following command within the directory `vagrant up`
3. The whole installation process will take up to 10 minutes. (1st setup only)

## If all else fail
1. Start a new ubuntu vm
2. sudo apt-get install the following packages:
    a. python3
    b. python-pip

3. Then install Scrapy using:
    a. `pip install scrapy`

