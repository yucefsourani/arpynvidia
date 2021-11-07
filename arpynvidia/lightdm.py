#!/usr/bin/env python3
from .util import isdual
import os
import subprocess
import configparser

config_file = "/etc/lightdm/lightdm.conf"
sh_file     = "/etc/lightdm/display_setup_arpynvidia.sh"

def lightdm_check():
    lines       = ["#!/bin/sh","xrandr --setprovideroutputsource modesetting NVIDIA-0","xrandr --auto"]
    if not os.path.isfile(sh_file):
        return False
    count       = 0
    try:
        with open(sh_file) as mf:
            for line in mf:
                if line.strip() in lines:
                    count+=1
    except Exception as e:
        print(e)
        print("Check Settings In {} Faild.".format(sh_file))
        return False
    if count >= 3:
        return True
    return False

def undo_lightdm_fix_optimus():
    try :
        with open(sh_file,"w") as mf:
            mf.write("")
    except Exception as e:
        print(e)
        print("Undo Settings In {} Faild.".format(sh_file))
        return False
    return True

def write_sh_file():
    if  os.path.isfile(sh_file):
        if lightdm_check():
            return True
        else:
            return __write_sh_file__()
    else:
        return __write_sh_file__()
        
def __write_sh_file__():
    sh_tor_write = """#!/bin/sh
xrandr --setprovideroutputsource modesetting NVIDIA-0
xrandr --auto
"""
    try:
        if os.path.isfile(sh_file):
            mode = "a"
        else:
            mode = "w"
        with open(sh_file,mode) as mf:
            mf.write(sh_tor_write)
    except Exception as e:
        print(e)
        print("Create {} Faild.".format(sh_file))
        return False
    return not subprocess.call("chmod +x {}".format(sh_file),shell=True)

def lightdm_fix_optimus():
    if not isdual():
        return True
    if not write_sh_file():
        return False
    modified    = False
    config      = configparser.ConfigParser(strict=False)
    try:
        config.read(config_file)
        if "Seat:*" not in config:
            config["Seat:*"] = {"display-setup-script" : sh_file}
            modified = True
        else:
            if config.has_option("Seat:*","display-setup-script"):
                if config.get("Seat:*","display-setup-script")!=sh_file:
                    config["Seat:*"]["display-setup-script"] = sh_file
                    modified = True
            else:
                config["Seat:*"]["display-setup-script"] = sh_file
                modified = True
        if modified:
            with open(config_file, 'w') as configfile:
                config.write(configfile)
    except Exception as e:
        print(e)
        print("Change Option In {} Faild.".format(config_file))
        return False
    return True
    
def _use_lightdm_():
    return lightdm_fix_optimus()
    
def _undo_use_lightdm_():
    return undo_lightdm_fix_optimus()

