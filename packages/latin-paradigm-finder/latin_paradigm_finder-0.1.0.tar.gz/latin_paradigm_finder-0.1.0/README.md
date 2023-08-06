## Latin paradigm translator

### Introduction

This code helps to find the paradigms present in a Latin version, and to create a text file of them.

It works by webscraping [Dizionario Latino Olivetti](https://www.dizionario-latino.com/) and checking if every word of the version is a verb. It can also find disambiguation pages and let you choose.

It makes a database where all  the words information is stored, so it doesn't webscrape too much.



#### Short video of how it works
<a href="https://asciinema.org/a/381561"><img src="https://asciinema.org/a/381561.png"></img></a>

### Installation

> The code is cross platform, I will soon upload how to install on Windows and MacOS

**Steps for Ubuntu 20.04**
#### Short video of the installation
<a href="https://asciinema.org/a/381560"><img src="https://asciinema.org/a/381560.png"></img></a>
1. Open a terminal with CTRL + ALT + T
2. Copy and paste these commands for installation

      `sudo apt-get install python3 python3-pip git`
	  
      `git clone https://github.com/bortox/latin_paradigm_finder && cd latin_paradigm_finder && sudo python3 setup.py install && cd ../ && sudo rm -rf latin_paradigm_finder`
   
### Open the program
**Type**  `paradigmi` in your terminal to open the program
###### Enjoy the time saved to you by this paradigm finder!
