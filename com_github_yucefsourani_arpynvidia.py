#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arpynvidiaservice.py
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
import dbus
import dbus.service
import dbus.mainloop.glib
import slip.dbus.service
import slip.dbus.polkit as polkit
from gi.repository import GLib
from arpynvidia.util    import get_displaymanger_name, issecureboot, enable_akmods_service,iswayland,isdual,check_if_installed
from arpynvidia.gdm     import _use_gdm_, _undo_use_gdm_
from arpynvidia.sddm    import _use_sddm_, _undo_use_sddm_
from arpynvidia.lightdm import _use_lightdm_, _undo_use_lightdm_
import subprocess
from arpynvidia.arpynvidialib import  get_info , get_info_with_update,get_ides_from_lspci
import threading
import os


def _use_xorg_():
    name = get_displaymanger_name()
    if not name:
        return False
    if "gdm" in name:
        return _use_gdm_()
    elif "sddm" in name:
        return _use_sddm_()
    elif "lightdm" in name:
        return _use_lightdm_()

def _undo_use_xorg_():
    name = get_displaymanger_name()
    if not name:
        return False
    if "gdm" in name:
        return _undo_use_gdm_()
    elif "sddm" in name:
        return _undo_use_sddm_()
    elif "lightdm" in name:
        return _undo_use_lightdm_()

class InstallDriverService(slip.dbus.service.Object):
    default_polkit_auth_required = "com.github.yucefsourani.arpynvidia.exec"
    def __init__(self,loop):
        self.__loop    = loop
        self.bus       = dbus.SystemBus()
        self.dbus_info = None
        self.polkit    = None
        self.__install_process     = None
        self.__undoinstall_process = None
        object_path    = "/com/github/yucefsourani/arpynvidia"
        #dbus.service.Object.__init__(self,conn=dbus.SessionBus(),object_path=object_path)
        bus_name    = dbus.service.BusName("com.github.yucefsourani.arpynvidia", self.bus)
        slip.dbus.service.Object.__init__(self,bus_name=bus_name,object_path=object_path)

    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='',out_signature='b')
    def EndInstall(self):
        if self.__install_process:
            if self.__install_process.poll() == None:
                self.__install_process.terminate()
                if self.__install_process.poll() == -15:
                    self.__install_process = None
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='',out_signature='b')
    def EndUndoInstall(self):
        if self.__undoinstall_process:
            if self.__undoinstall_process.poll() == None:
                self.__undoinstall_process.terminate()
                if self.__undoinstall_process.poll() == -15:
                    self.__undoinstall_process = None
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True
        
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='',out_signature='s')
    def GetDisplayMangerName(self):
        return get_displaymanger_name()
    
    @polkit.require_auth("com.github.yucefsourani.arpynvidia.exec")
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='',out_signature='b')
    def EnableAkmodsService(self):
        return enable_akmods_service()
        
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='',out_signature='b')
    def IsDualVga(self):
        return isdual()

    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='',out_signature='b',sender_keyword="sender",connection_keyword="conn")
    def IsWayland(self,sender=None, conn=None):
        #if not self.__check_polkit_privilege(sender,conn):
        #    return
        return iswayland()
        
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='',out_signature='b')
    def IsSecureBoot(self):
        return issecureboot()

    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='',out_signature='b')
    def IsNvidiaAvailable(self):
        if len(get_ides_from_lspci()) != 0:
            return True
        else:
            return False
            
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='as',out_signature='b')
    def CheckIfInstalled(self,packages):
        return check_if_installed(packages)
            
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='b',out_signature='')
    def GetNvidiaInfo(self,with_lib32):
        threading.Thread(target=self.__GetNvidiaInfo,args=(with_lib32,)).start()
        
    def __GetNvidiaInfo(self,with_lib32):
        result = get_info(with_lib32)
        self.OnGetInfoDOne(result)
        
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='b',out_signature='')
    def GetNvidiaInfoWithUpdate(self,with_lib32):
        threading.Thread(target=self.__GetNvidiaInfoWithUpdate,args=(with_lib32,)).start()
        
    def __GetNvidiaInfoWithUpdate(self,with_lib32):
        result =  get_info_with_update(with_lib32)
        self.OnGetInfoDOne(result)

    
    @polkit.require_auth("com.github.yucefsourani.arpynvidia.exec")
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='s',out_signature='')
    def Install(self,driver_packages_name):
        if self.__install_process!=None:
            return
        if self.__undoinstall_process != None:
            return 
        threading.Thread(target=self.__Install,args=(driver_packages_name,)).start()
    
    def __Install(self,driver_packages_name):
        out = subprocess.Popen("dnf update kernel -b -y",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        self.__install_process = out
        while out.poll()==None:
            out.stdout.flush()
            line = out.stdout.readline().decode("utf-8").strip()
            if line:
                self.OnInstallOutput(line)
        self.__install_process = None
        out = subprocess.Popen("dnf install {} -b -y".format(driver_packages_name),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        self.__install_process = out
        while out.poll()==None:
            out.stdout.flush()
            line = out.stdout.readline().decode("utf-8").strip()
            if line:
                self.OnInstallOutput(line)
        self.__install_process = None
        result1 = not out.poll()
        result2 = _use_xorg_()
        result3 = enable_akmods_service()
        self.InstallResult((result1,result2,result3))


    @polkit.require_auth("com.github.yucefsourani.arpynvidia.exec")
    @dbus.service.method(dbus_interface='com.github.yucefsourani.arpynvidia',
                         in_signature='s',out_signature='')
    def UndoInstall(self,driver_packages_name):
        if self.__undoinstall_process != None:
            return
        if self.__install_process != None:
            return 
        driver_packages_name = driver_packages_name.replace("kernel-devel","").replace("kernel","")
        threading.Thread(target=self.__undo,args=(driver_packages_name,)).start()
    
    def __undo(self,driver_packages_name):
        out = subprocess.Popen("dnf remove {} --noautoremove -y".format(driver_packages_name),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        self.__undoinstall_process = out
        while out.poll()==None:
            out.stdout.flush()
            line = out.stdout.readline().decode("utf-8").strip()
            if line:
                self.OnUndoInstallOutput(line)
        self.__undoinstall_process = None
        result1 = not out.poll()
        result2 = _undo_use_xorg_()
        self.UndoInstallResult((result1,result2))


    @dbus.service.signal(dbus_interface='com.github.yucefsourani.arpynvidia',
                         signature='ab')
    def InstallResult(self, var):
        # run just before the signal is actually emitted
        # just put "pass" if nothing should happen
        pass

    @dbus.service.signal(dbus_interface='com.github.yucefsourani.arpynvidia',
                         signature='ab')
    def UndoInstallResult(self, var):
        # run just before the signal is actually emitted
        # just put "pass" if nothing should happen
        pass

    @dbus.service.signal(dbus_interface='com.github.yucefsourani.arpynvidia',
                         signature='as')
    def OnGetInfoDOne(self, var):
        # run just before the signal is actually emitted
        # just put "pass" if nothing should happen
        pass
        
    @dbus.service.signal(dbus_interface='com.github.yucefsourani.arpynvidia',
                         signature='s')
    def OnUndoInstallOutput(self, var):
        # run just before the signal is actually emitted
        # just put "pass" if nothing should happen
        pass

    @dbus.service.signal(dbus_interface='com.github.yucefsourani.arpynvidia',
                         signature='s')
    def OnInstallOutput(self, var):
        # run just before the signal is actually emitted
        # just put "pass" if nothing should happen
        pass

    """def __check_polkit_privilege(self, sender, conn):
        # Get Peer PID
        if self.dbus_info is None:
            # Get DBus Interface and get info thru that
            self.dbus_info = dbus.Interface(conn.get_object("org.freedesktop.DBus",
                                                            "/org/freedesktop/DBus/Bus", False),
                                            "org.freedesktop.DBus")
        pid = self.dbus_info.GetConnectionUnixProcessID(sender)
     
        # Query polkit
        if self.polkit is None:
            self.polkit = dbus.Interface(dbus.SystemBus().get_object(
            "org.freedesktop.PolicyKit1",
            "/org/freedesktop/PolicyKit1/Authority", False),
                                         "org.freedesktop.PolicyKit1.Authority")
     
        # Check auth against polkit; if it times out, try again
        try:
            auth_response = self.polkit.CheckAuthorization(
                ("unix-process", {"pid": dbus.UInt32(pid, variant_level=1),
                                  "start-time": dbus.UInt64(0, variant_level=1)}),
                "com.github.yucefsourani.arpynvidia.exec", {"AllowUserInteraction": "true"}, dbus.UInt32(1), "", timeout=600)
            print(auth_response)
            (is_auth, _, details) = auth_response
        except dbus.DBusException as e:
            if e._dbus_error_name == "org.freedesktop.DBus.Error.ServiceUnknown":
                # polkitd timeout, retry
                self.polkit = None
                return self.__check_polkit_privilege(sender, conn, privilege)
            else:
                # it's another error, propagate it
                raise
     
        if not is_auth:
            # Aww, not authorized :(
            print(":(")
            return False
     
        print("Successful authorization!")
        return True"""
            
if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    dbus.mainloop.glib.threads_init()
    loop = GLib.MainLoop()
    slip.dbus.service.set_mainloop(loop)
    installdriverservice = InstallDriverService(loop)
    loop.run()
