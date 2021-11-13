# arpynvidia BETA (For Fedora Linux Only)
Gui Program To Install Nvidia Driver From rpmfusion 

برنامج لتثبيت تعريف كرت الشاشة نفيديا من مستودعات rpmfusion


Warning !! Use This Program on Your own Risk

Tested Only On Fedora 35  Workstation with Nvidia Optimus.


إستخدم هذا البرنامج على مسؤوليتك وقد جرب فقط على فيدورا 35 بواجهة جنوم بجهاز يحتوي كرت نفيديا هجين


https://arfedora.blogspot.com


# Requires

 * xrandr
 * python3-gobject
 * gtk3
 * python3-slip
 * python3-slip-dbus
 * python3-dbus
 * python3-beautifulsoup4
 * rpmfusion-nonfree (rpmfusion repos)

# To Install
``` git clone  https://github.com/yucefsourani/arpynvidia ```

``` cd arpynvidia ```

``` sudo ./setup.py install --prefix=/usr ```

``` sudo systemctl reload dbus.service ```


![Alt text](https://raw.githubusercontent.com/yucefsourani/arpynvidia/main/Screenshot_1.jpg "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/arpynvidia/main/Screenshot_2.jpg "Screenshot")
