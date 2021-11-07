#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arpynvidia.py
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
#  fix gdm -- check lightdm -- package on copr

import dbus
from slip.dbus import polkit
import dbus.mainloop.glib
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk , GLib, Gio, GdkPixbuf, Gdk
import threading
import os
import sys

css = b"""
        .h1 {
            font-size: 24px;
        }
        .h2 {
            font-weight: 300;
            font-size: 18px;
        }
        .h3 {
            font-size: 11px;
        }
        .h4 {
            color: alpha (@text_color, 0.7);
            font-weight: bold;
            text-shadow: 0 1px @text_shadow_color;
        }
        .h4 {
            padding-bottom: 6px;
            padding-top: 6px;
        }
        textview text {
          background-color: black;
        }
        """
class YesOrNo(Gtk.MessageDialog):
    def __init__(self,msg,parent=None):
        Gtk.MessageDialog.__init__(self,buttons = Gtk.ButtonsType.OK_CANCEL)
        self.props.message_type = Gtk.MessageType.QUESTION
        self.props.text         = msg
        self.p=parent
        if self.p != None:
            self.parent=self.p
            self.set_transient_for(self.p)
            self.set_modal(True)
            self.p.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
            
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.OK:
            self.destroy()
            if self.p != None:
                self.p.set_sensitive(True)
            return True
        else:
            if self.p != None:
                self.p.set_sensitive(True)
            self.destroy()
            return False
            
class ArPyNvidiaProxy(object):

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.dbus_object = self.bus.get_object(
            "com.github.yucefsourani.arpynvidia",
            "/com/github/yucefsourani/arpynvidia")

    @polkit.enable_proxy
    def GetDisplayMangerName(self):
        return self.dbus_object.GetDisplayMangerName(
            dbus_interface="com.github.yucefsourani.arpynvidia")

    @polkit.enable_proxy
    def EnableAkmodsService(self):
        return self.dbus_object.EnableAkmodsService(
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def IsDualVga(self):
        return self.dbus_object.IsDualVga(
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def IsWayland(self):
        return self.dbus_object.IsWayland(
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def IsSecureBoot(self):
        return self.dbus_object.IsSecureBoot(
            dbus_interface="com.github.yucefsourani.arpynvidia")

    @polkit.enable_proxy
    def CheckIfInstalled(self,packages):
        return self.dbus_object.CheckIfInstalled(
            packages,
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def GetNvidiaInfo(self,with_lib32=True):
        return self.dbus_object.GetNvidiaInfo(
            with_lib32 ,
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def GetNvidiaInfoWithUpdate(self,with_lib32=True):
        return self.dbus_object.GetNvidiaInfoWithUpdate(
            with_lib32 ,
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def Install(self,driver_packages_name):
        return self.dbus_object.Install(
            driver_packages_name,
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def UndoInstall(self,driver_packages_name):
        return self.dbus_object.UndoInstall(
            driver_packages_name ,
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def IsSecureBoot(self):
        return self.dbus_object.IsSecureBoot(
            dbus_interface="com.github.yucefsourani.arpynvidia")

    @polkit.enable_proxy
    def IsNvidiaAvailable(self):
        return self.dbus_object.IsNvidiaAvailable(
            dbus_interface="com.github.yucefsourani.arpynvidia")

    @polkit.enable_proxy
    def EndInstall(self):
        return self.dbus_object.EndInstall(
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    @polkit.enable_proxy
    def EndUndoInstall(self):
        return self.dbus_object.EndUndoInstall(
            dbus_interface="com.github.yucefsourani.arpynvidia")
            
    def connect_to_signal(self,signal,callback,arg0=None):
        if arg0 != None:
            return self.dbus_object.connect_to_signal(signal, callback, dbus_interface="com.github.yucefsourani.arpynvidia",arg0=arg0)
        else:
            return self.dbus_object.connect_to_signal(signal, callback, dbus_interface="com.github.yucefsourani.arpynvidia")


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

def get_correct_path(relative_path):
    exedir = os.path.dirname(sys.argv[0])
    p      = os.path.join(exedir,'..', 'share/arpynvidia/')
    if not os.path.exists(p):
        base_path = exedir
    else :
        base_path = p
    return os.path.join(base_path, relative_path)


class CTextView():
    def __init__(self):
        self.sw = Gtk.ScrolledWindow()        
        self.t = Gtk.TextView()
        self.textviewbuffer          = self.t.get_buffer()
        self.t.props.editable        = False
        self.t.props.cursor_visible  = False
        self.t.props.justification   = Gtk.Justification.LEFT
        self.t.props.wrap_mode       = Gtk.WrapMode.CHAR
        self.sw.add(self.t)
        self.t.connect("size-allocate", self._autoscroll)
        self.t.set_sensitive(False)
        
    def _autoscroll(self,widget,rec):
        adj = self.sw.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def insert_text(self,text):
        self.textviewbuffer.insert_at_cursor(text,len(text))
        
class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("ArPyNvidia")
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)        
        self.set_size_request(800, 650)
        self.mainvbox = Gtk.VBox()
        self.mainvbox.props.margin = 10
        self.mainvbox.props.spacing = 10
        self.add(self.mainvbox)
        self.packages = ("","")
        self.lock = False
        
        self.arpynvidia_proxy = ArPyNvidiaProxy()

        try:
            if  not self.arpynvidia_proxy.IsNvidiaAvailable():
                err_label = Gtk.Label()
                err_label.get_style_context().add_class("h1")
                err_label.props.wrap = True
                err_label.props.label = "No Nvidia Card Detected"
                self.mainvbox.add(err_label)
                return
        except Exception as e:
            err_label = Gtk.Label()
            err_label.get_style_context().add_class("h1")
            err_label.props.wrap = True
            err_label.props.label = "NotAuthorizedException"
            self.mainvbox.add(err_label)
            print(e)
            return
        try:
            self.displaymanager = self.arpynvidia_proxy.GetDisplayMangerName()
            if self.displaymanager not in ("gdm","sddm","lightdm") and self.arpynvidia_proxy.IsDualVga():
                err_label = Gtk.Label()
                err_label.get_style_context().add_class("h1")
                err_label.props.wrap = True
                err_label.props.label = "Error! Display Manager {} Not Supported.".format(displaymanager)
                self.mainvbox.add(err_label)
                return
        except Exception as e:
            err_label = Gtk.Label()
            err_label.get_style_context().add_class("h1")
            err_label.props.wrap = True
            err_label.props.label = "NotAuthorizedException"
            self.mainvbox.add(err_label)
            print(e)
            return 
        try:
            if  self.arpynvidia_proxy.IsSecureBoot():
                err_label = Gtk.Label()
                err_label.get_style_context().add_class("h1")
                err_label.props.wrap = True
                err_label.props.label = "Error! Please Disable SecureBoot"
                self.mainvbox.add(err_label)
                return
        except Exception as e:
            err_label = Gtk.Label()
            err_label.get_style_context().add_class("h1")
            err_label.props.wrap = True
            err_label.props.label = "NotAuthorizedException"
            self.mainvbox.add(err_label)
            print(e)
            return 
            

        
        
        self.driver_need_install = True
        
        self.spinner = Gtk.Spinner()
        self.spinner.start()
        self.mainvbox.add(self.spinner)
        
        self.arpynvidia_proxy.connect_to_signal("OnGetInfoDOne",self.on_get_info_done)
        try:
            self.arpynvidia_proxy.GetNvidiaInfoWithUpdate(True)
        except Exception as e:
            self.spinner.stop()
            self.mainvbox.remove(self.spinner)
            err_label = Gtk.Label()
            err_label.get_style_context().add_class("h1")
            err_label.props.wrap = True
            err_label.props.label = "Gettings Drive Info Faild"
            self.mainvbox.add(err_label)
            print(e)

    def on_get_info_done(self,result):
        self.packages = result
        self.spinner.stop()
        self.mainvbox.remove(self.spinner)
        if not result[1]: # result[1] == str packages to install 
            err_label = Gtk.Label()
            err_label.get_style_context().add_class("h1")
            err_label.props.wrap = True
            err_label.props.label = "Gettings Drive Info Faild\nCheck Your Internet Connection\nTry Install rpmfusion repos"
            self.mainvbox.add(err_label)
            self.show_all()
        elif result[1] == "NODRIVER":
            err_label = Gtk.Label()
            err_label.get_style_context().add_class("h1")
            err_label.props.wrap = True
            err_label.props.label = "No Driver Found\nTry Install rpmfusion repos"
            self.mainvbox.add(err_label)
            self.show_all()
        else:
            if self.arpynvidia_proxy.CheckIfInstalled(result[1].replace("kernel-devel","").replace("kernel","").split()):
                self.driver_need_install = False
            self.gui()
        
    def gui(self):
        self.infobar = Gtk.InfoBar()
        self.infobar_content = self.infobar.get_content_area()
        self.infobar_label = Gtk.Label()
        self.infobar_content.add(self.infobar_label)
        self.infobar.props.no_show_all = True
        self.infobar.set_message_type(Gtk.MessageType.INFO)
        self.infobar.set_show_close_button(True)
        self.infobar.connect("response", self.hide__infobar)
        self.mainvbox.pack_start(self.infobar,False,False,1)
        
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(get_correct_path("images/NVLogo_2D.png"),200,200,True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.mainvbox.pack_start(image,False,False,1)
        
        name_label = Gtk.Label()
        name_label.get_style_context().add_class("h1")
        name_label.props.wrap = True
        name_label.props.label = self.packages[0]
        self.mainvbox.pack_start(name_label,False,False,1)

        self.install_remove_button = Gtk.Button()
        self.install_remove_button.get_style_context().add_class("destructive-action")
        if self.driver_need_install:
            self.install_remove_button.props.label = "Install Driver"
        else:
            self.install_remove_button.props.label = "Remove Driver"
            
        self.install_remove_button.connect("clicked",self.on_button_clicked)
        self.mainvbox.pack_start(self.install_remove_button,False,False,1)
        
        self.textview = CTextView()
        self.mainvbox.pack_start(self.textview.sw,True,True,1)
        
        self.show_all()

    def on_button_clicked(self,button):
        if self.driver_need_install:
            yon = YesOrNo("Continue Install Driver?",self)
            if not yon.check():
                return
        else:
            yon = YesOrNo("Continue Remove Driver?",self)
            if not yon.check():
                return
        self.lock = True
        self.infobar.hide()
        threading.Thread(target=self._on_button_clicked).start()
        
    def _on_button_clicked(self):
        if self.driver_need_install:
            self.install_driver()
        else:
            self.remove_driver()
        
    def on_install_remove_output(self,text):
        GLib.idle_add(self.textview.insert_text,text+"\n")
        
    def on_install_remove_finish(self,result):
        self.lock = False
        GLib.idle_add(self.install_remove_button.set_sensitive,True)
        if result[0]:
            if self.driver_need_install:
                self.install_remove_button.props.label = "Remove Driver"
                self.driver_need_install = False
                if self.displaymanager != "gdm":
                    self.show_in_infobar("Please Reboot System.\nAnd Change session in {} to use x11|xorg".format(self.displaymanager))
                else:
                    self.show_in_infobar("Please Reboot System.")
            else:
                self.install_remove_button.props.label = "Install Driver"
                self.driver_need_install = True
                self.show_in_infobar("Please Reboot System.")
        else:
            if self.driver_need_install:
                self.show_in_infobar("Install Driver Faild.")
            else:
                self.show_in_infobar("Remove Driver Faild.")

    def install_driver(self):
        GLib.idle_add(self.install_remove_button.set_sensitive,False)
        try:
            self.arpynvidia_proxy.connect_to_signal("OnInstallOutput",self.on_install_remove_output)
            self.arpynvidia_proxy.connect_to_signal("InstallResult",self.on_install_remove_finish)
            self.arpynvidia_proxy.Install(self.packages[1])
        except Exception as e:
            print(e)
            GLib.idle_add(self.install_remove_button.set_sensitive,True)

    def remove_driver(self):
        GLib.idle_add(self.install_remove_button.set_sensitive,False)
        try:
            self.arpynvidia_proxy.connect_to_signal("OnUndoInstallOutput",self.on_install_remove_output)
            self.arpynvidia_proxy.connect_to_signal("UndoInstallResult",self.on_install_remove_finish)
            self.arpynvidia_proxy.UndoInstall(self.packages[1])
        except Exception as e:
            print(e)
            GLib.idle_add(self.install_remove_button.set_sensitive,True)

    def hide__infobar(self, infobar=None, respose_id=None):
        self.infobar.hide()
        
    def show_in_infobar(self, text):
        self.infobar_label.props.label = text
        self.infobar_content.show_all()
        self.infobar.show()

        
        
def on_quit_(self,event,mainwindow):
    if mainwindow.lock:
        return True
    Gtk.main_quit()
    
mainwindow = MainWindow()
mainwindow.connect("delete-event",on_quit_,mainwindow)
mainwindow.show_all()
Gtk.main()
