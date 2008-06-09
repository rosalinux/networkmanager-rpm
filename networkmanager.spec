%define libnm_glib           %mklibname nm_glib 0
%define libnm_glib_devel     %mklibname nm_glib -d
%define libnm_glib_vpn       %mklibname nm_glib_vpn 0
%define libnm_glib_vpn_devel %mklibname nm_glib_vpn -d
%define libnm_util           %mklibname nm_util 0
%define libnm_util_devel     %mklibname nm_util -d

ExcludeArch: s390 s390x

%define dbus_version 1.1
%define dbus_glib_version 0.73-6
%define hal_version 0.5.0

%define gtk2_version 2.12.0
%define wireless_tools_version 1:28-0pre9
%define libnl_version 1.0-0.15.pre8.git20071218
%define ppp_version 2.2.4

%define snapshot svn3669
%define applet_snapshot svn724

Name: networkmanager
Summary: Network connection manager and user applications
Epoch: 1
Version: 0.7.0
Release: %mkrel 0.9.3.%{snapshot}.2
Group: System/Base
License: GPLv2+
URL: http://www.gnome.org/projects/NetworkManager/
Source: NetworkManager-%{version}.%{snapshot}.tar.gz
Source1: nm-applet-%{version}.%{applet_snapshot}.tar.gz
Source2: nm-system-settings.conf
Patch1: NetworkManager-0.6.5-fixup-internal-applet-build.patch
Patch3: optionally-wait-for-network.patch
Patch4: serial-debug.patch
Patch5: explain-dns1-dns2.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: hal >= %{hal_version}
Requires: iproute2 openssl
Requires: dhcp-client >= 3.0.2-12
Requires: wpa_supplicant >= 0.5.7-21
#Requires: libnl >= %{libnl_version}
Requires: %{name}-glib = %{epoch}:%{version}-%{release}
Requires: ppp >= %{ppp_version}
#Obsoletes: dhcdbd

# Due to VPN auth-dialog changes in applet r662
Conflicts: NetworkManager-vpnc < 1:0.7.0-0.7.7.svn3549
Conflicts: NetworkManager-openvpn < 1:0.7.0-9.svn3549

BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: libiw-devel >= %{wireless_tools_version}
BuildRequires: hal-devel >= %{hal_version}
BuildRequires: glib2-devel gtk2-devel
BuildRequires: libglade2.0-devel
BuildRequires: openssl-devel
BuildRequires: libGConf2-devel
BuildRequires: gnome-panel-devel
BuildRequires: gnomeui2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: wpa_supplicant
BuildRequires: libnl-devel >= %{libnl_version}
BuildRequires: libnotify-devel >= 0.3
BuildRequires: perl(XML::Parser)
BuildRequires: automake autoconf intltool libtool
BuildRequires: ppp-devel >= %{ppp_version}
BuildRequires: nss-devel >= 3.11.7
BuildRequires: polkit-devel policykit-gnome-devel
Provides: NetworkManager = %{epoch}:%{version}-%{release}

%description
NetworkManager attempts to keep an active network connection available at all
times.  It is intended only for the desktop use-case, and is not intended for
usage on servers.   The point of NetworkManager is to make networking
configuration and setup as painless and automatic as possible.  If using DHCP,
NetworkManager is _intended_ to replace default routes, obtain IP addresses
from a DHCP server, and change nameservers whenever it sees fit.


%package -n %{libnm_util}
Summary: Shared library for nm_util
Group: System/Libraries
Obsoletes: %{mklibname networkmanager-util 0} < %{epoch}:%{version}-%{release}

%description -n %{libnm_util}
Shared library for nm_util.


%package -n nm-applet
Summary: GNOME applications for use with NetworkManager
Group: Networking/Other
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-glib = %{epoch}:%{version}-%{release}
#Requires: gnome-panel
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: hal >= %{hal_version}
#Requires: libnotify >= 0.3
Requires(post): gtk+2 >= %{gtk2_version}
Requires(postun): gtk+2 >= %{gtk2_version}
Requires: gnome-keyring
Requires: nss >= 3.11.7
Requires: gnome-icon-theme
Provides: NetworkManager-gnome = %{epoch}:%{version}-%{release}
Provides: %{name}-gnome = %{epoch}:%{version}-%{release}

%description -n nm-applet
This package contains GNOME utilities and applications for use with
NetworkManager, including a panel applet for wireless networks.


%package devel
Summary: Libraries and headers for adding NetworkManager support to applications
Group: Development/C
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: dbus-devel >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: pkgconfig
Provides: NetworkManager-devel = %{epoch}:%{version}-%{release}
Requires: %{libnm_util_devel} = %{epoch}:%{version}-%{release}

%description devel
This package contains various headers accessing some NetworkManager
functionality from applications.


%package -n %{libnm_util_devel}
Summary: Development files for nm_util
Group: Development/C
Obsoletes: %{mklibname networkmanager-util 0 -d} < %{epoch}:%{version}-%{release}
Provides: libnm_util-devel = %{epoch}:%{version}-%{release}

%description -n %{libnm_util_devel}
Development files for nm_util.


%package glib
Summary: Libraries for adding NetworkManager support to applications that use glib
Group: Development/C
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Provides: NetworkManager-glib = %{epoch}:%{version}-%{release}
Requires: %{libnm_glib} = %{epoch}:%{version}-%{release}
Requires: %{libnm_glib_vpn} = %{epoch}:%{version}-%{release}

%description glib
This package contains the libraries that make it easier to use some
NetworkManager functionality from applications that use glib.


%package -n %{libnm_glib}
Summary: Shared library for nm_glib
Group: System/Libraries
Obsoletes: %{mklibname networkmanager-glib 0} < %{epoch}:%{version}-%{release}

%description -n %{libnm_glib}
Shared library for nm_glib.


%package -n %{libnm_glib_vpn}
Summary: Shared library for nm_glib_vpn
Group: System/Libraries

%description -n %{libnm_glib_vpn}
Shared library for nm_glib_vpn.


%package glib-devel
Summary: Header files for adding NetworkManager support to applications that use glib
Group: Development/C
Requires: %{name}-devel = %{epoch}:%{version}-%{release}
Requires: %{name}-glib = %{epoch}:%{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig
Requires: dbus-glib-devel >= %{dbus_glib_version}
Provides: NetworkManager-glib-devel = %{epoch}:%{version}-%{release}
Requires: %{libnm_glib_devel} = %{epoch}:%{version}-%{release}
Requires: %{libnm_glib_vpn_devel} = %{epoch}:%{version}-%{release}

%description glib-devel
This package contains the header and pkg-config files for development
applications using NetworkManager functionality from applications that use
glib.


%package -n %{libnm_glib_devel}
Summary: Development files for nm_glib
Group: Development/C
Provides: nm_glib-devel = %{epoch}:%{version}-%{release}
Obsoletes: %{mklibname networkmanager-glib 0 -d} < %{epoch}:%{version}-%{release}

%description -n %{libnm_glib_devel}
Development files for nm_glib.


%package -n %{libnm_glib_vpn_devel}
Summary: Development files for nm_glib_vpn
Group: Development/C
Provides: nm_glib_vpn-devel = %{epoch}:%{version}-%{release}

%description -n %{libnm_glib_vpn_devel}
Development files for nm_glib_vpn.


%prep
%setup -q -n NetworkManager-%{version}

# unpack the applet
tar -xzf %{SOURCE1}
%patch1 -p1 -b .buildfix
%patch3 -p1 -b .wait-for-network
%patch4 -p1 -b .serial-debug
%patch5 -p1 -b .explain-dns1-dns2

%build
# Even though we don't require named, we still build with it
# so that if the user installs it, NM will use it automatically
autoreconf -i
%configure2_5x \
        --disable-static \
        --with-named=/usr/sbin/named \
        --with-named-dir=/var/named/data \
        --with-named-user=named
make

# build the applet
pushd nm-applet-0.7.0
  autoreconf -i
  intltoolize --force
  %configure2_5x \
        --disable-static \
    --with-notify \
    --with-nss=yes \
    --with-gnutls=no
  make
popd
 
%install
%{__rm} -rf $RPM_BUILD_ROOT

# install NM
%makeinstall_std

%{__cp} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/

# install the applet
pushd nm-applet-0.7.0
  %makeinstall_std
popd

# create a VPN directory
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/VPN

%find_lang NetworkManager
%find_lang nm-applet

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/pppd/2.4.4/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/NetworkManager/*.la

install -m 0755 test/.libs/nm-online %{buildroot}/%{_bindir}

%clean
%{__rm} -rf $RPM_BUILD_ROOT


%post
%_post_service %{name}

%preun
%_preun_service %{name}

%if %mdkversion < 200900
%post -n %{libnm_util} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libnm_util} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libnm_glib} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libnm_glib} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libnm_glib_vpn} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libnm_glib_vpn} -p /sbin/ldconfig
%endif

%post -n nm-applet
%update_icon_cache hicolor

%postun -n nm-applet
%clean_icon_cache hicolor

%files -f NetworkManager.lang
%defattr(-,root,root,0755)
%doc COPYING ChangeLog NEWS AUTHORS README CONTRIBUTING TODO
%{_sysconfdir}/dbus-1/system.d/NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-dhcp-client.conf
%{_sysconfdir}/dbus-1/system.d/nm-dispatcher.conf
%{_sysconfdir}/dbus-1/system.d/nm-system-settings.conf
%attr(0755,root,root) %{_initrddir}/%{name}
%{_sbindir}/NetworkManager
%{_sbindir}/nm-system-settings
%config(noreplace) %{_sysconfdir}/nm-system-settings.conf
%dir %{_sysconfdir}/NetworkManager/
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%dir %{_sysconfdir}/NetworkManager/VPN
%{_bindir}/nm-tool
%{_bindir}/nm-online
%{_libdir}/nm-dhcp-client.action
%{_libdir}/nm-dispatcher.action
%dir %{_libdir}/NetworkManager
%{_libdir}/NetworkManager/*.so*
%{_mandir}/man1/*
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/run/NetworkManager
%{_libdir}/nm-crash-logger
%dir %{_datadir}/NetworkManager
%{_datadir}/NetworkManager/gdb-cmd
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManagerSystemSettings.service
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_libdir}/pppd/2.4.4/nm-pppd-plugin.so
%{_datadir}/PolicyKit/policy/*.policy

%files -n %{libnm_util}
%defattr(-,root,root,0755)
%{_libdir}/libnm-util.so.*

%files -n nm-applet -f nm-applet.lang
%defattr(-,root,root,0755)
%{_sysconfdir}/dbus-1/system.d/nm-applet.conf
%{_bindir}/nm-applet
%{_bindir}/nm-vpn-properties
%{_bindir}/nm-connection-editor
%{_datadir}/gnome-vpn-properties/nm-vpn-properties.glade
%{_datadir}/nm-applet/
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%config(noreplace) %{_sysconfdir}/xdg/autostart/nm-applet.desktop

%files devel
%defattr(-,root,root,0755)
%dir %{_includedir}/NetworkManager
%{_includedir}/NetworkManager/*.h
%{_libdir}/pkgconfig/NetworkManager.pc

%files -n %{libnm_util_devel}
%defattr(-,root,root,0755)
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-util.so

%files glib
%defattr(-,root,root,0755)

%files -n %{libnm_glib}
%defattr(-,root,root,0755)
%{_libdir}/libnm_glib.so.*

%files -n %{libnm_glib_vpn}
%defattr(-,root,root,0755)
%{_libdir}/libnm_glib_vpn.so.*

%files glib-devel
%defattr(-,root,root,0755)

%files -n %{libnm_glib_devel}
%defattr(-,root,root,0755)
%dir %{_includedir}/libnm-glib
%{_includedir}/libnm-glib/*.h
%{_libdir}/pkgconfig/libnm_glib.pc
%{_libdir}/libnm_glib.so

%files -n %{libnm_glib_vpn_devel}
%defattr(-,root,root,0755)
%{_libdir}/libnm_glib_vpn.so
