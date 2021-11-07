#!/usr/bin/env python3
from .util import iswayland, isdual
import os
import configparser

config_file = "/etc/gdm/custom.conf"

def undo_gdm_fix_optimus():
    files = ["/usr/share/gdm/greeter/autostart/optimus.desktop" ,"/etc/xdg/autostart/optimus.desktop"]
    for file_ in files:
        if  os.path.isfile(file_):
            try:
                os.system("rm {}".format(file_))
            except Exception as e:
                print(e)
                print("Remove {} Faild.".format(file_))
                return False
    return True
    
def gdm_fix_optimus():
    if not isdual():
        return True
    to_write = """[Desktop Entry]
Type=Application
Name=Optimus
Exec=sh -c "xrandr --setprovideroutputsource modesetting NVIDIA-0; xrandr --auto"
NoDisplay=true
X-GNOME-Autostart-Phase=DisplayServer
"""
    files = ["/usr/share/gdm/greeter/autostart/optimus.desktop" ,"/etc/xdg/autostart/optimus.desktop"]
    for file_ in files:
        if not os.path.isfile(file_):
            try:
                with open(file_,"w") as mf:
                    mf.write(to_write)
            except Exception as e:
                print(e)
                print("Create {} Faild.".format(file_))
                return False
    return True
    
def gdm_use_change_display_server():
    modified    = False
    config      = configparser.ConfigParser(strict=False)
    config.optionxform = lambda option: option 
    try:
        config.read(config_file)
        if "daemon" not in config:
            config.add_section("daemon")
            #config["daemon"] = {"waylandenable" : "false"}
            config.set("daemon","WaylandEnable","false")
            modified = True
        else:
            if config.has_option("daemon","WaylandEnable"):
                config.set("daemon","WaylandEnable","false")
                #config["daemon"]["waylandenable"] = "false"
                modified = True
            elif config.has_option("daemon","waylandenable"):
                config.set("daemon","waylandenable","false")
                #config["daemon"]["waylandenable"] = "false"
                modified = True
            else:
                #config["daemon"]["WaylandEnable"] = "false"
                config.set("daemon","WaylandEnable","false")
                modified = True
        if modified:
            with open(config_file, 'w') as mf:
                config.write(mf)
    except Exception as e:
        print(e)
        print("Change Option In {} Faild.".format(config_file))
        return False
    return True

def gdm_undo_change_display_server():
    modified    = False
    config      = configparser.ConfigParser(strict=False)
    config.optionxform = lambda option: option 
    try:
        config.read(config_file)
        if "daemon" not in config:
            config.add_section("daemon")
            #config["daemon"] = {"waylandenable" : "true"}
            config.set("daemon","WaylandEnable","true")
            modified = True
        else:
            if config.has_option("daemon","WaylandEnable"):
                config.set("daemon","WaylandEnable","true")
                #config["daemon"]["WaylandEnable"] = "true"
                modified = True
            elif config.has_option("daemon","waylandenable"):
                config.set("daemon","waylandenable","true")
                #config["daemon"]["waylandenable"] = "true"
                modified = True
            else:
                #config["daemon"]["WaylandEnable"] = "true"
                config.set("daemon","WaylandEnable","true")
                modified = True
        if modified:
            with open(config_file, 'w') as mf:
                config.write(mf)
    except Exception as e:
        print(e)
        print("Change Option In {} Faild.".format(config_file))
        return False
    return True
    
def _use_gdm_(fixwayland=True):
    if fixwayland:
        ot1 = gdm_use_change_display_server()
        if not ot1:
            print("Set GDM Settings Faild.")
            return False
    ot2 =  gdm_fix_optimus()
    if not ot2:
        print("Set Optimus Settings Faild.")
        return False
    return True
    
def _undo_use_gdm_(fixwayland=True):
    if fixwayland:
        ot1 = gdm_undo_change_display_server()
        if not ot1:
            print("Undo GDM Settings Faild.")
            return False
    ot2 =  undo_gdm_fix_optimus()
    if not ot2:
        print("Undo Optimus Settings Faild.")
        return False
    return True


