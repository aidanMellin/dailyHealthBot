# dailyHealthBot
An auto running python based daily health screen completion tool for RIT

For this program you are going to need a few different packages:

pip -> sudo apt-get install python-pip
selenium -> pip install selenium
tkinter -> sudo apt-get install python-tkinter

xming (possibly) -> 'https://sourceforge.net/projects/xming/'

I HAVE INCLUDED DRIVERS FOR SELENIUM FOR BOTH CHROME AND FIREFOX AS THEY ARE THE MOST POPULAR:
You will need to add these to your PATH in order to execute this program

This program can be wonky on first run. There are some methods of attack in this situation:
1. If you are operating this through windows (typically through WSL), you can use xming, and then simply
    i. xhost +
    ii. export DISPLAY=localhost:0.0
2. If that's a bit too much for you, you can manually update the secrets.txt file included. 
    i. You will need to upload your username and password to the text file, and I would then recommend that you change the browser to 'Firefox' as that has been the primary mode of development

