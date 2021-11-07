#!/usr/bin/env python3
from .util import iswayland, isdual
import os

config_file = "/etc/sddm/Xsetup"
lines       = ["xrandr --setprovideroutputsource modesetting NVIDIA-0","xrandr --auto"]

def sddm_check():
    if not os.path.isfile(config_file):
        return False
    count       = 0
    try:
        with open(config_file) as mf:
            for line in mf:
                if line.strip() in lines:
                    count+=1
    except Exception as e:
        print(e)
        return False
    if count >= 2:
        return True
    return False


def undo_sddm_fix_optimus():
    if not sddm_check():
        return True
    result       = ""
    try:
        with open(config_file) as mf:
            for line in mf:
                l = line.strip()
                if l in lines:
                    continue
                result += line
        with open(config_file,"w") as mf:
            mf.write(result)
    except Exception as e:
        print(e)
        return False
    return True
    
def sddm_fix_optimus():
    if not isdual():
        return True
    if sddm_check():
        return True
    try:
        if os.path.isfile(config_file):
            mode = "a"
        else:
            mode = "w"
        with open(config_file,mode) as mf:
            for line in lines:
                mf.write(line+"\n")
    except Exception as e:
        print(e)
        return False
    return True


def _use_sddm_():
    return sddm_fix_optimus()
    
def _undo_use_sddm_():
    return undo_sddm_fix_optimus()
