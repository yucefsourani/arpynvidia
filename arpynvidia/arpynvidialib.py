#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arnvidialib.py
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
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json

home           = os.getenv("HOME")
DATALOCATION   = os.path.join(home,".config","arpynvidia")
os.makedirs(DATALOCATION,exist_ok=True)

def __get_all_available_nvidia_driver__():
    result = {}
    output = subprocess.check_output("pkexec dnf repoquery --disablerepo=* --enablerepo=rpmfusion-nonfree-updates,rpmfusion-nonfree \"*nvidia*\" |grep -i akmod-nvidia-",shell=True).decode("utf-8").split("\n")
    for driver_package_name in output:
        if driver_package_name:
            driver_package_name = driver_package_name.split(":")
            driver_number       = driver_package_name[1].split("-")[0]
            driver_package_name = driver_package_name[0]+":"+driver_number
            result.setdefault(driver_number,driver_package_name)
    return result

def dump_to_json(file_l,dict_,indent=4):
    try:
        with open(file_l,"w") as mf:
            json.dump(dict_,mf,indent=indent)
    except:
        return False
    return True
    
def get_all_available_nvidia_driver():
    packages_info = os.path.join(DATALOCATION,"packages_info.json")
    if os.path.isfile(packages_info):
        try:
            with open(packages_info) as json_f:
                result = json.load(json_f)
        except:
            result = __get_all_available_nvidia_driver__()
            dump_to_json(packages_info,result)
    else:
        result = __get_all_available_nvidia_driver__()
        dump_to_json(packages_info,result)
    return result
            
def get_and_update_driver_info_by_number(driver_number,agent="Mozilla/5.0"):
    data_file_location = os.path.join(DATALOCATION,driver_number+".ids")
    link = "http://us.download.nvidia.com/XFree86/Linux-x86_64/{}/README/supportedchips.html".format(driver_number)
    try:
        url   = Request(link,headers={"User-Agent":agent})
        opurl = urlopen(url)
        data  = opurl.read().decode("utf-8")
        with open(data_file_location,"w") as mf:
            mf.write(data)
    except Exception as e :
        print(e)
        return False
    opurl.close()
    return data_file_location

def get_driver_by_number(driver_number,agent="Mozilla/5.0",force=False):
    data_file_location = os.path.join(DATALOCATION,driver_number+".ids")
    if not force:
        if not os.path.isfile(data_file_location):
            data_file_location = get_and_update_driver_info_by_number(driver_number,agent)
    else:
        data_file_location = get_and_update_driver_info_by_number(driver_number,agent)
    return data_file_location

def old_extract_drive_info(driver_number,agent="Mozilla/5.0"):
    data_file_location = os.path.join(DATALOCATION,driver_number+".ids")
    if not os.path.isfile(data_file_location):
        check = get_driver_by_number(driver_number,agent=agent)
        if not check:
            return False
    result = []
    try:
        with open(data_file_location) as mf:
            soup = BeautifulSoup(mf,"html.parser")
            for tr in soup.findAll("tr"):
                try:
                    res = tr.attrs["id"]
                    if res.startswith("devid"):
                        res = res[5:]
                    elif res.startswith("0x"):
                        res = res[2:]
                    res = res.split("_")
                    for i in res:
                        result.append(i)
                except:
                    continue
    except Exception as e:
        print(e)
        return False
    return result


def update_pciids(agent="Mozilla/5.0"):
    data_file_location = os.path.join(DATALOCATION,"pci.ids")
    link  = "http://pciids.sourceforge.net/pci.ids"
    try:
        url   = Request(link,headers={"User-Agent":agent})
        opurl = urlopen(link)
        data  = opurl.read().decode("utf-8")
        with open(data_file_location,"w") as mf:
            mf.write(data)
    except Exception as e:
        print(e)
        return False
    opurl.close()
    return True
    
def get_ides_from_lspci(id_="10de"):
    lspci = subprocess.Popen(["lspci", "-n"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split("\n")
    lspci = [i.split()[2].split(":")[1].lower() for i in lspci if i if i.split()[2].split(":")[0].lower()==id_]
    #lspci.append("2208".lower()) # to testing
    return lspci

def found_in_pci_ids(id_="10de"):
    data_file_location = os.path.join(DATALOCATION,"pci.ids")
    if not os.path.isfile(data_file_location):
        check = update_pciids()
        if not check :
            return False
    b = False
    result = {}
    with open(data_file_location) as mf:
        for line in mf:
            line  = line.rstrip()
            if line.startswith(id_):
                b = True
                continue
            elif b and not line.startswith("\t") :
                if not line.startswith("#"):
                    b = False
            if b :
                if not line.startswith("\t\t") and line.startswith("\t"):
                    linestripsplit = line.lstrip().split(" ",1)
                    result.setdefault(linestripsplit[0],linestripsplit[1])
    return result

def extract_drive_info(driver_number="470.74",agent="Mozilla/5.0",force=False):
    data_file_location = os.path.join(DATALOCATION,driver_number+".ids")
    if not force:
        if not os.path.isfile(data_file_location):
            check = get_driver_by_number(driver_number,agent=agent)
            if not check:
                return False
    else:
        check = get_driver_by_number(driver_number,agent,force)
        if not check:
            return False
    result = []
    text = ""
    try:
        with open(data_file_location) as mf:
            for i in mf:
                if "longer" in i:
                    text+="\n</body>\n"
                    text+="</html>"
                    break
                text+=i
            soup = BeautifulSoup(text,"html.parser")
            for tr in soup.findAll("tr"):
                try:
                    res = tr.attrs["id"]
                    if res.startswith("devid"):
                        res = res[5:]
                    elif res.startswith("0x"):
                        res = res[2:]
                    res = res.split("_")
                    for i in res:
                        result.append(i)
                except:
                    continue
    except Exception as e:
        print(e)
        return False
    return result

def get_vga_name_by_id(id_):
    try:
        name = found_in_pci_ids()[id_]
    except Exception as e:
        print(e)
        name = ""
    return name


def get_info(lib32=True):
    lspci_ids = get_ides_from_lspci()
    if lspci_ids:
        all_driver_info = get_all_available_nvidia_driver()
        if not all_driver_info:
            return ("NODRIVER","NODRIVER")
        for driver_number in sorted(all_driver_info.keys(),reverse=True):
            driver_package_name = all_driver_info[driver_number]
            ids = extract_drive_info(driver_number)
            if not ids:
                return False
            for id_ in lspci_ids:
                if id_ in ids:
                    name = get_vga_name_by_id(id_)
                    if not name:
                        return False
                    if lib32:
                        return (name,"xorg-x11-drv-nvidia-"+driver_number.split(".",1)[0]+"xx" + " kernel kernel-devel " + driver_package_name+" xorg-x11-drv-nvidia-"+driver_number.split(".",1)[0]+"xx-libs.i686")
                    else:
                        return (name,"xorg-x11-drv-nvidia-"+driver_number.split(".",1)[0]+"xx" + " kernel kernel-devel"+driver_package_name)
    return ("NODRIVER","NODRIVER")
    
def get_info_with_update(lib32=True):
    check = update_pciids()
    if not check:
        return False        
    lspci_ids = get_ides_from_lspci()
    if lspci_ids:
        all_driver_info = get_all_available_nvidia_driver()
        if not all_driver_info:
            return ("NODRIVER","NODRIVER")
        for driver_number in sorted(all_driver_info.keys(),reverse=True):
            driver_package_name = all_driver_info[driver_number]
            ids = extract_drive_info(driver_number,force=True)
            if not ids:
                return False
            for id_ in lspci_ids:
                if id_ in ids:
                    name = get_vga_name_by_id(id_)
                    if not name:
                        return False
                    if lib32:
                        return (name,"xorg-x11-drv-nvidia-"+driver_number.split(".",1)[0]+"xx" + " kernel kernel-devel " + driver_package_name+" xorg-x11-drv-nvidia-"+driver_number.split(".",1)[0]+"xx-libs.i686")
                    else:
                        return (name,"xorg-x11-drv-nvidia-"+driver_number.split(".",1)[0]+"xx" + " kernel kernel-devel"+driver_package_name)
    return ("NODRIVER","NODRIVER")
    


if __name__ == "__main__":
    print(get_ides_from_lspci())
