%define name networkmanager
%define rname NetworkManager
%define version 0.6.4
%define release %mkrel 6

%define glib_name     %{name}-glib
%define util_name     %{name}-util

%define glib_major 0
%define util_major 0

%define lib_glib_name %mklibname %{glib_name} %{glib_major}
%define lib_util_name %mklibname %{util_name} %{util_major}

Summary: NetworkManager
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{rname}-%{version}.tar.bz2
Patch0: NetworkManager-0.6.4-linux_if.patch
Patch1: NetworkManager-0.6.4-close.patch
Patch2: NetworkManager-dbus-dcl.patch
License: GPL
Group: System/Configuration/Networking
Url: http://www.gnome.org/projects/NetworkManager/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libnl-devel
BuildRequires: dhcdbd
BuildRequires: wpa_supplicant
BuildRequires: libiw-devel
BuildRequires: perl(XML::Parser)
BuildRequires: hal-devel >= 0.5.0
BuildRequires: libglade2.0-devel
BuildRequires: libGConf2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: dbus-glib-devel
BuildRequires: gnome-panel-devel
Requires: dhcdbd wpa_supplicant wireless-tools
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
NetworkManager attempts to keep an active network connection available
at all times.  The point of NetworkManager is to make networking
configuration and setup as painless and automatic as possible.  If
using DHCP, NetworkManager is _intended_ to replace default routes,
obtain IP addresses from a DHCP server, and change nameservers
whenever it sees fit.  In effect, the goal of NetworkManager is to
make networking Just Work.

%package -n %{lib_glib_name}
Group: System/Libraries
Summary: Library for %{glib_name}
%description -n %{lib_glib_name}
Library for %{glib_name}.

%package -n %{lib_util_name}
Group: System/Libraries
Summary: Library for %{util_name}
%description -n %{lib_util_name}
Library for %{util_name}.

%package -n %{lib_glib_name}-devel
Group: Development/C
Summary: Devel library for %{glib_name}
Provides: lib%{glib_name}-devel = %{version}-%{release}
Requires: %{lib_glib_name} = %{version}
%description -n %{lib_glib_name}-devel
Devel library for %{glib_name}.

%package -n %{lib_util_name}-devel
Group: Development/C
Summary: Devel library for %{util_name}
Provides: lib%{util_name}-devel = %{version}-%{release}
Requires: %{lib_util_name} = %{version}
%description -n %{lib_util_name}-devel
Devel library for %{util_name}.

%package devel
Group: Development/C
Summary: Devel library for %{rname}
%description devel
Devel library for %{rname}.

%prep
%setup -q -n %{rname}-%{version}
%patch0 -p1 -b .linux_if
%patch1 -p1 -b .close
%patch2 -p0 -b .dbus-dcl

%build
%configure2_5x --localstatedir=%{_var}
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
%find_lang %{rname}

%clean
rm -rf $RPM_BUILD_ROOT


%post
%_post_service %{rname}
%_post_service %{rname}Dispatcher
%update_icon_cache hicolor

%postun
%clean_icon_cache hicolor

%preun
%_preun_service %{rname}Dispatcher
%_preun_service %{rname}

%post -n %{lib_glib_name} -p /sbin/ldconfig
%postun -n %{lib_glib_name} -p /sbin/ldconfig

%post -n %{lib_util_name} -p /sbin/ldconfig
%postun -n %{lib_util_name} -p /sbin/ldconfig


%files -f %{rname}.lang
%defattr(-,root,root)
%doc AUTHORS CONTRIBUTING ChangeLog NEWS README TODO
%{_bindir}/nm-applet
%{_bindir}/nm-vpn-properties
%{_sbindir}/%{rname}
%{_sbindir}/%{rname}Dispatcher
%{_initrddir}/%{rname}
%{_initrddir}/%{rname}Dispatcher
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/%{rname}.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/nm-applet.conf
%dir %{_sysconfdir}/%{rname}
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%dir %{_var}/run/%{rname}
%{_libdir}/nm-crash-logger
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/gnome/autostart/nm-applet.desktop
%dir %{_datadir}/%{rname}
%{_datadir}/%{rname}/*
%dir %{_datadir}/nm-applet
%{_datadir}/nm-applet/applet.glade
%{_datadir}/nm-applet/keyring.png
%dir %{_datadir}/gnome-vpn-properties
%{_datadir}/gnome-vpn-properties/nm-vpn-properties.glade
%{_mandir}/man1/*.1*

%files -n %{lib_glib_name}
%{_libdir}/libnm_glib.so.*

%files -n %{lib_util_name}
%{_libdir}/libnm-util.so.*


%files devel
%dir %{_includedir}/%{rname}
%{_includedir}/%{rname}/%{rname}*.h
%{_includedir}/%{rname}/nm-vpn-ui-interface.h
%{_libdir}/pkgconfig/%{rname}.pc

%files -n %{lib_glib_name}-devel
%{_includedir}/%{rname}/libnm_glib.h
%{_libdir}/libnm_glib.so
%{_libdir}/libnm_glib.la
%{_libdir}/libnm_glib.a
%{_libdir}/pkgconfig/libnm_glib.pc

%files -n %{lib_util_name}-devel
%{_includedir}/%{rname}/cipher*.h
%{_includedir}/%{rname}/dbus-*.h
%{_libdir}/libnm-util.so
%{_libdir}/libnm-util.la
%{_libdir}/libnm-util.a
%{_libdir}/pkgconfig/libnm-util.pc


