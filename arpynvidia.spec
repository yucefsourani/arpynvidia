Name:           arpynvidia
Version:        1.0
Release:        1%{?dist}
Summary:        Nvidia Driver Installer
License:        GPLv3     
URL:            https://github.com/yucefsourani/arpynvidia
Source0:        https://github.com/yucefsourani/arpynvidia/archive/refs/heads/main.zip
BuildArch:      noarch
BuildRequires:  python3-devel
#BuildRequires:  gettext
Requires:       python3-gobject
Requires:       gtk3
#Requires:       gettext
Requires:       python3-slip
Requires:       python3-slip-dbus
Requires:       python3-dbus
Requires:       python3-beautifulsoup4
Requires:       xrandr

%description
Nvidia Driver Installer For Fedora Linux.


%prep
%autosetup -n arpynvidia-main

%build
%{__python3} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT --prefix /usr

#%find_lang %{name}

#%files -f %{name}.lang
%files
%doc README.md LICENSE
%{python3_sitelib}/*
%{python3_sitelib}/arpynvidia/*
%{_bindir}/arpynvidia.py
%{_datadir}/applications/com.github.yucefsourani.arpynvidia.desktop
%{_datadir}/arpynvidia/*
%{_datadir}/arpynvidia/images/*
%{_datadir}/pixmaps/com.github.yucefsourani.arpynvidia.png
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/polkit-1/actions/com.github.yucefsourani.arpynvidia.policy
%{_datadir}/dbus-1/system-services/com.github.yucefsourani.arpynvidia.service
%{_libexecdir}/com_github_yucefsourani_arpynvidia.py
%{_sysconfdir}/dbus-1/system.d/com.github.yucefsourani.arpynvidia.conf

%changelog
* San Jun 07 2021 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-1
- Initial For Fedora 

