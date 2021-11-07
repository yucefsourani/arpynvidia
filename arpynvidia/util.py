#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  util.py
#  
#  Copyright 2021 yucef sourni <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import subprocess
import os
import configparser

system_arch    = os.uname().machine
distro_desktop = os.getenv("XDG_CURRENT_DESKTOP","")

if distro_desktop:
    distro_desktop = distro_desktop.lower()

def iswayland():
    xdg_session = os.getenv("XDG_SESSION_TYPE")
    if not xdg_session:
        return False
    if "wayland" in xdg_session.lower():
        return True
    return False
    
def isdual():
    out=subprocess.Popen("lspci -nn | egrep -i \"3d|display|vga\"",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
    if len([i for i in out.decode("utf-8").split("\n") if i])==2:
        return True
    return False
    
def issecureboot():
    out = subprocess.Popen("mokutil --sb-state",shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
    if out == "SecureBoot enabled":
        return True
    else:
        return False

def get_displaymanger_name():
    try:
        config_data = subprocess.check_output("systemctl cat display-manager.service --no-pager",shell=True).decode("utf-8")
        config      = configparser.ConfigParser(strict=False)
        config.read_string(config_data)
        name        = os.path.basename(config["Service"]["ExecStart"]).lower()
    except:
        name = ""
    return name

def enable_akmods_service():
    return not subprocess.call("systemctl enable akmods.service",shell=True)

def check_if_installed(packages):
    packages = " ".join(packages)
    return not subprocess.call("rpm -q {}".format(packages),shell=True)
    

