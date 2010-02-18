%define _requires_exceptions devel\(libnss3.*\)\\|devel\(libnspr4.*\)\\|devel\(libsmime3.*\)

%define	major_glib	2
%define major_glib_vpn	1
%define major_util	1
%define libnm_glib		%mklibname nm-glib %{major_glib}
%define libnm_glib_devel	%mklibname -d nm-glib
%define libnm_glib_vpn		%mklibname nm-glib-vpn %{major_glib_vpn}
%define libnm_glib_vpn_devel	%mklibname -d nm-glib-vpn
%define libnm_util		%mklibname nm-util %{major_util}
%define libnm_util_devel	%mklibname -d nm-util

%define snapshot 0

%define	rname	NetworkManager
Name:		networkmanager
Summary:	Network connection manager and user applications
Version:	0.7.999
%if %{snapshot}
Release:	%mkrel 0.%{snapshot}.1
%else
Release:        %mkrel 3
%endif
Group:		System/Base
License:	GPLv2+
URL:		http://www.gnome.org/projects/NetworkManager/
%if %snapshot
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.7/%{rname}-%{version}.%{snapshot}.tar.xz
%else
Source0:        http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.7/%{rname}-%{version}.tar.bz2
Source1:	README.urpmi
%endif
# This patch is build from GIT at git://git.mandriva.com/projects/networkmanager.git
# DO NOT CHANGE IT MANUALLY.
# To generate patch use
#	git diff master..mdv
# Current mdv tip: 329ddd9
Patch1:		networkmanager-mdv.patch
# Fedora patches
Patch2:		explain-dns1-dns2.patch
# (fhimpe) Make it use correct location for dhclient lease files
BuildRequires:	libnl-devel wpa_supplicant libiw-devel dbus-glib-devel
BuildRequires:	hal-devel >= 0.5.0 nss-devel intltool
BuildRequires:	gtk-doc ext2fs-devel
BuildRequires:	ppp-devel polkit-1-devel 
BuildRequires:	libuuid-devel
BuildRequires:	libgudev-devel
BuildRequires:	dhcp-client
BuildRequires:	iptables
Requires:	wpa_supplicant wireless-tools dhcp-client
Requires:	mobile-broadband-provider-info
Requires:	modemmanager
Requires:	dhcp-client
Requires:	dnsmasq-base
Requires:	ppp = %(rpm -q --queryformat "%{VERSION}" ppp )
Requires:	iproute2
Requires:	iptables
Provides:	NetworkManager = %{version}-%{release}
Obsoletes:	dhcdbd
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Conflicts:	%{_lib}nm_util1 < 0.7.996
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
Obsoletes:	%{_lib}nm_util1 < 0.7.996
Provides:	%{_lib}nm_util1 = %{version}-%{release}

%description -n %{libnm_util}
Shared library for nm-util.

%package -n	%{libnm_util_devel}
Summary:	Development files for nm_util
Group:		Development/C
Obsoletes:	%{mklibname networkmanager-util 0 -d}
Provides:	libnm-util-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	NetworkManager-devel = %{version}-%{release}
Requires:	%{libnm_util} = %version-%release
Obsoletes:	%{_lib}nm_util-devel < 0.7.996

%description -n %{libnm_util_devel}
Development files for nm-util.

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
Provides:	libnm-glib-devel = %{version}-%{release}
Provides:       NetworkManager-glib-devel = %{version}-%{release}
Obsoletes:	%{mklibname networkmanager-glib 0 -d}
Requires:	%{libnm_glib} = %version-%release
Obsoletes:	%{_lib}nm_glib-devel < 0.7.996

%description -n %{libnm_glib_devel}
Development files for nm-glib.

%package -n	%{libnm_glib_vpn}
Summary:	Shared library for nm-glib-vpn
Group:		System/Libraries
Conflicts:	%{_lib}nm-glib1 < 0.7.996

%description -n	%{libnm_glib_vpn}
This package contains the libraries that make it easier to use some
NetworkManager VPN functionality from applications that use glib.

%package -n	%{libnm_glib_vpn_devel}
Summary:	Development files for nm-glib-vpn
Group:		Development/C
Provides:	libnm-glib-vpn-devel = %{version}-%{release}
Requires:	%{libnm_glib_vpn} = %version-%release
Conflicts:	%{_lib}nm_glib-devel < 0.7.996

%description -n %{libnm_glib_vpn_devel}
Development files for nm-glib-vpn.

%prep
%setup -q -n %{rname}-%{version}
%patch1 -p1 -b .networkmanager-mdv
%patch2 -p1 -b .explain-dns1-dns2

%build

autoreconf -fis
%configure2_5x	--disable-static \
		--with-distro=mandriva \
		--with-dhcp-client=dhclient \
		--with-crypto=nss \
		--enable-more-warnings=yes \
		--with-docs=yes \
		--with-system-ca-path=/etc/pki/tls/certs \
		--with-resolvconf=yes \
		--with-tests=yes

%make

%install
rm -rf %{buildroot}
%makeinstall_std

cat > %{buildroot}%{_sysconfdir}/NetworkManager/nm-system-settings.conf << EOF
[main]
plugins=ifcfg-mdv
EOF

# create a VPN directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/VPN
install -m755 test/.libs/nm-online -D %{buildroot}%{_bindir}/nm-online

# create keyfile plugin system-settings directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/system-connections

# Add readme displayed by urpmi
cp %{SOURCE1} .

%find_lang %{rname}

find %{buildroot} -name \*.la|xargs rm -f

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files -f %{rname}.lang
%defattr(-,root,root)
%doc AUTHORS CONTRIBUTING ChangeLog NEWS README TODO
%doc README.urpmi
%{_sysconfdir}/dbus-1/system.d/NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-avahi-autoipd.conf
%{_sysconfdir}/dbus-1/system.d/nm-dhcp-client.conf
%{_sysconfdir}/dbus-1/system.d/nm-dispatcher.conf
%{_initrddir}/%{name}
#%{_initrddir}/%{rname}dispatcher
%dir %{_sysconfdir}/%{rname}
%config(noreplace) %{_sysconfdir}/%{rname}/nm-system-settings.conf
%{_sbindir}/%{rname}
#%{_sbindir}/%{rname}Dispatcher
%dir %{_sysconfdir}/%{rname}
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%dir %{_sysconfdir}/%{rname}/system-connections
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
%{_libdir}/pppd/*.*.*/nm-pppd-plugin.so
%dir %{_localstatedir}/run/%{rname}
%{_libexecdir}/nm-crash-logger
%dir %{_datadir}/%{rname}
%{_datadir}/%{rname}/gdb-cmd
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/polkit-1/actions/org.freedesktop.network-manager-settings.system.policy
%{_datadir}/gtk-doc/html/*
/lib/udev/rules.d/*.rules

%files -n %{libnm_util}
%defattr(-,root,root)
%{_libdir}/libnm-util.so.%{major_util}*

%files -n %{libnm_util_devel}
%defattr(-,root,root)
%dir %{_includedir}/%{rname}
%{_includedir}/%{rname}/*.h
%{_libdir}/pkgconfig/%{rname}.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-util.so

%files -n %{libnm_glib}
%defattr(-,root,root)
%{_libdir}/libnm-glib.so.%{major_glib}*

%files -n %{libnm_glib_vpn}
%defattr(-,root,root)
%{_libdir}/libnm-glib-vpn.so.%{major_glib_vpn}*

%files -n %{libnm_glib_devel}
%defattr(-,root,root)
%dir %{_includedir}/libnm-glib
%exclude %{_includedir}/libnm-glib/nm-vpn*.h
%{_includedir}/libnm-glib/*.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/libnm-glib.so

%files -n %{libnm_glib_vpn_devel}
%defattr(-,root,root)
%{_includedir}/libnm-glib/nm-vpn*.h
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/libnm-glib-vpn.so

