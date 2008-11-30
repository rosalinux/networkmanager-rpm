%define _requires_exceptions devel\(libnss3.*\)\\|devel\(libnspr4.*\)\\|devel\(libsmime3.*\)

%define	major	0
%define libnm_glib           %mklibname nm_glib %{major}
%define libnm_glib_devel     %mklibname -d nm_glib
%define libnm_util           %mklibname nm_util %{major}
%define libnm_util_devel     %mklibname -d nm_util

%define	rname	NetworkManager
Name:		networkmanager
Summary:	Network connection manager and user applications
Version:	0.7.0
Release:	%mkrel 2
Group:		System/Base
License:	GPLv2+
URL:		http://www.gnome.org/projects/NetworkManager/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.7/%{rname}-%{version}.tar.bz2
BuildRequires:	libnl-devel wpa_supplicant libiw-devel dbus-glib-devel
BuildRequires:	hal-devel >= 0.5.0 nss-devel intltool
BuildRequires:	gtk-doc ext2fs-devel
BuildRequires:	ppp-devel polkit-devel policykit-gnome-devel
Requires:	wpa_supplicant wireless-tools dhcp-client
Provides:	NetworkManager = %{name}-%{version}
Obsoletes:	dhcdbd
Requires(post):	rpm-helper
Requires(preun):rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
NetworkManager attempts to keep an active network connection available at all
times.  It is intended only for the desktop use-case, and is not intended for
usage on servers.   The point of NetworkManager is to make networking
configuration and setup as painless and automatic as possible.  If using DHCP,
NetworkManager is _intended_ to replace default routes, obtain IP addresses
from a DHCP server, and change nameservers whenever it sees fit.

%package -n	%{libnm_util}
Summary:	Shared library for nm_util
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-util 0}

%description -n %{libnm_util}
Shared library for nm_util.

%package -n	%{libnm_util_devel}
Summary:	Development files for nm_util
Group:		Development/C
Obsoletes:	%{mklibname networkmanager-util 0 -d}
Provides:	libnm_util-devel = %{version}-%{release}
Provides:	%{name}-devel = %{name}-%{version}
Provides:	NetworkManager-devel = %{name}-%{version}
Requires:	%libnm_util = %version-%release

%description -n %{libnm_util_devel}
Development files for nm_util.

%package -n	%{libnm_glib}
Summary:	Shared library for nm_glib
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-glib 0}

%description -n	%{libnm_glib}
This package contains the libraries that make it easier to use some
NetworkManager functionality from applications that use glib.

%package -n	%{libnm_glib_devel}
Summary:	Development files for nm_glib
Group:		Development/C
Provides:	libnm_glib-devel = %{version}-%{release}
Provides:       NetworkManager-glib-devel = %{name}-%{version}
Obsoletes:	%{mklibname networkmanager-glib 0 -d}
Requires:	%libnm_glib = %version-%release

%description -n %{libnm_glib_devel}
Development files for nm_glib.

%prep
%setup -q -n %{rname}-%{version}
autoreconf -i

%build
%configure2_5x	--disable-static \
		--with-distro=mandriva
%make

%install
rm -rf %{buildroot}
%makeinstall_std

cat > %{buildroot}%{_sysconfdir}/nm-system-settings.conf << EOF
[main]
plugins=ifcfg-fedora
EOF

# create a VPN directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/VPN
install -m755 test/.libs/nm-online -D %{buildroot}%{_bindir}/nm-online

%find_lang %{rname}

find %{buildroot} -name \*.la|xargs rm -f

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%if %mdkversion < 200900
%post -n %{libnm_util} -p /sbin/ldconfig
%postun -n %{libnm_util} -p /sbin/ldconfig
%post -n %{libnm_glib} -p /sbin/ldconfig
%postun -n %{libnm_glib} -p /sbin/ldconfig
%endif

%files -f %{rname}.lang
%defattr(-,root,root)
%doc AUTHORS CONTRIBUTING ChangeLog NEWS README TODO
%{_sysconfdir}/dbus-1/system.d/NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-avahi-autoipd.conf
%{_sysconfdir}/dbus-1/system.d/nm-dhcp-client.conf
%{_sysconfdir}/dbus-1/system.d/nm-dispatcher.conf
%{_sysconfdir}/dbus-1/system.d/nm-system-settings.conf
%{_initrddir}/%{name}
#%{_initrddir}/%{rname}dispatcher
%{_sbindir}/nm-system-settings
%{_sysconfdir}/nm-system-settings.conf
%{_sbindir}/%{rname}
#%{_sbindir}/%{rname}Dispatcher
%dir %{_sysconfdir}/%{rname}
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%dir %{_sysconfdir}/NetworkManager/VPN
%{_bindir}/nm-tool
%{_bindir}/nm-online
%{_libdir}/nm-dispatcher.action
%{_libexecdir}/nm-dhcp-client.action
%{_libexecdir}/nm-avahi-autoipd.action
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*
%dir %{_libdir}/NetworkManager
%{_libdir}/NetworkManager/*.so
%dir %{_localstatedir}/run/%{rname}
%{_libexecdir}/nm-crash-logger
%dir %{_datadir}/%{rname}
%{_datadir}/%{rname}/gdb-cmd
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManagerSystemSettings.service
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/PolicyKit/policy/*.policy
%{_datadir}/gtk-doc/html/*

%files -n %{libnm_util}
%defattr(-,root,root)
%{_libdir}/libnm-util.so.%{major}*
%{_libdir}/pppd/*.*.*/nm-pppd-plugin.so

%files -n %{libnm_util_devel}
%defattr(-,root,root)
%dir %{_includedir}/%{rname}
%{_includedir}/%{rname}/*.h
%{_libdir}/pkgconfig/%{rname}.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-util.so

%files -n %{libnm_glib}
%defattr(-,root,root)
%{_libdir}/libnm_glib.so.%{major}*
%{_libdir}/libnm_glib_vpn.so.%{major}*

%files -n %{libnm_glib_devel}
%defattr(-,root,root)
%dir %{_includedir}/libnm-glib
%{_includedir}/libnm-glib/*.h
%{_libdir}/pkgconfig/libnm_glib.pc
%{_libdir}/pkgconfig/libnm_glib_vpn.pc
%{_libdir}/libnm_glib.so
%{_libdir}/libnm_glib_vpn.so
