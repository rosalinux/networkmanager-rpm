%define	url_ver %(echo %{version}|cut -d. -f1,2)

#define	snapshot 0
%define	rname	NetworkManager
%define	api	1.0

%define	majglib		4
%define	libnm_glib	%mklibname nm-glib %{majglib}
%define	girclient	%mklibname	nmclient-gir %{api}
%define	devnm_glib	%mklibname -d nm-glib

%define	majvpn		1
%define	libnm_glib_vpn	%mklibname nm-glib-vpn %{majvpn}
%define	devnm_glib_vpn	%mklibname -d nm-glib-vpn
	
%define	majutil		2
%define	libnm_util	%mklibname nm-util %{majutil}
%define	girname		%mklibname	%{name}-gir %{api}
%define	devnm_util	%mklibname -d nm-util


Name:		networkmanager
Summary:	Network connection manager and user applications
Version:	0.9.8.10
Release:	1
Group:		System/Base
License:	GPLv2+
Url:		http://www.gnome.org/projects/NetworkManager/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/%{url_ver}/%{rname}-%{version}%{?snapshot:.%{snapshot}}.tar.xz
Source1:	README.urpmi
# XXX: repository MIA?? patch manually regenerated...
# This patch is build from GIT at git://git.mandriva.com/projects/networkmanager.git
# DO NOT CHANGE IT MANUALLY.
# To generate patch use
#	git diff master..mdv
# Current mdv tip: 2e93ff7
Patch1:		networkmanager-0.9.8.0-mdv.patch
# Fedora patches
Patch2:		networkmanager-0.8.1.999-explain-dns1-dns2.patch
# Mandriva specific patches
Patch50:	networkmanager-0.9.2.0-systemd-start-after-resolvconf.patch
Patch51:	networkmanager-0.9.8.4-add-systemd-alias.patch
Patch10:	nm-polkit-permissive.patch
# fixed Patch52:	networkmanager-fix-includes.patch
Patch63:	NetworkManager-0.9.4.0-dhcpcd-verbose-output.patch
Patch64:	NetworkManager-0.9.3.995-discover-mac-address.patch
# taken from Mageia
Patch65:	NetworkManager-0.9.3.990-mga-wireless_essid.patch
Patch66:	NetworkManager-0.9.8.8-prefer-dhcpcd-over-dhclient.patch
Patch67:	NetworkManager-0.9.8.8-disable-dhcpcd-ipv6-for-now-untill-remaining-support-is-in-place.patch

# upstream patches
Patch107:	networkmanager-0.9.4.0-nm-remote-settings.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	iptables
BuildRequires:	systemd-units
BuildRequires:	wpa_supplicant
BuildRequires:	libiw-devel
BuildRequires:	ppp-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(glibmm-2.4)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(mm-glib)

Requires:	dhcp-client-daemon
Requires:	dnsmasq-base
Requires:	iproute2
Requires:	iptables
Requires:	mobile-broadband-provider-info
Requires:	modemmanager
Requires:	ppp = %(rpm -q --queryformat "%{VERSION}" ppp )
Requires(post,preun,postun):	rpm-helper
Requires:	wireless-tools
Requires:	wpa_supplicant >= 0.7.3-2
Suggests:	nscd
Provides:	NetworkManager = %{EVRD}
Obsoletes:	dhcdbd
Conflicts:	%{_lib}nm_util1 < 0.7.996
Conflicts:	initscripts < 9.24-5

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
%rename		%{_lib}nm_util1

%description -n	%{libnm_util}
Shared library for nm-util.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}nm-util2 < 0.9.8.0-2

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n	%{devnm_util}
Summary:	Development files for nm_util
Group:		Development/C
Obsoletes:	%{mklibname networkmanager-util 0 -d}
Provides:	nm-util-devel = %{EVRD}
Requires:	%{libnm_util} = %{EVRD}
Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{_lib}nm_util-devel < 0.7.996

%description -n	%{devnm_util}
Development files for nm-util.

%package -n	%{libnm_glib}
Summary:	Shared library for nm_glib
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-glib 0}

%description -n	%{libnm_glib}
This package contains the libraries that make it easier to use some
NetworkManager functionality from applications that use glib.

%package -n %{girclient}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}nm-glib4 < 0.9.8.0-2

%description -n %{girclient}
GObject Introspection interface description for %{name}.

%package -n	%{devnm_glib}
Summary:	Development files for nm_glib
Group:		Development/C
Provides:	nm-glib-devel = %{EVRD}
Requires:	%{libnm_glib} = %{EVRD}
Requires:	%{girclient} = %{version}-%{release}
Obsoletes:	%{mklibname networkmanager-glib 0 -d}
Obsoletes:	%{_lib}nm_glib-devel < 0.7.996

%description -n	%{devnm_glib}
Development files for nm-glib.

%package -n	%{libnm_glib_vpn}
Summary:	Shared library for nm-glib-vpn
Group:		System/Libraries
Conflicts:	%{_lib}nm-glib1 < 0.7.996

%description -n	%{libnm_glib_vpn}
This package contains the libraries that make it easier to use some
NetworkManager VPN functionality from applications that use glib.

%package -n	%{devnm_glib_vpn}
Summary:	Development files for nm-glib-vpn
Group:		Development/C
Provides:	nm-glib-vpn-devel = %{EVRD}
Requires:	%{libnm_glib_vpn} = %{EVRD}
Conflicts:	%{_lib}nm_glib-devel < 0.7.996

%description -n	%{devnm_glib_vpn}
Development files for nm-glib-vpn.

%prep
%setup -qn %{rname}-%{version}
%apply_patches
autoreconf -fi
intltoolize -f

%build
%define	_disable_ld_no_undefined 1
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--with-crypto=nss \
	--enable-more-warnings=no \
	--with-docs=yes \
	--with-system-ca-path=%{_sysconfdir}/pki/tls/certs \
	--with-resolvconf=yes \
	--with-session-tracking=systemd \
	--with-suspend-resume=systemd \
	--with-systemdsystemunitdir=%{_systemunitdir} \
	--with-tests=yes \
	--with-dhcpcd=/sbin/dhcpcd \
	--with-dhclient=/sbin/dhclient \
	--with-iptables=/sbin/iptables \
	--with-resolvconf=/sbin/resolvconf \
	--enable-polkit \
	--enable-ppp \
	--enable-concheck \
	--with-wext=yes \
	--enable-modify-system \
	--with-modem-manager-1=yes

%make

%install
%makeinstall_std

# ifcfg-mdv currently broken, so just use ifcfg-rh for now untill it gets fixed
cat > %{buildroot}%{_sysconfdir}/NetworkManager/NetworkManager.conf << EOF
[main]
plugins=ifcfg-mdv,keyfile
EOF

# create a VPN directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/VPN
install -m755 test/.libs/nm-online -D %{buildroot}%{_bindir}/nm-online

# create keyfile plugin system-settings directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/system-connections

# Add readme displayed by urpmi
cp %{SOURCE1} .

# link service file to match alias
ln -sf %{_systemunitdir}/%{rname}.service %{buildroot}%{_systemunitdir}/%{name}.service

# (bor) clean up on uninstall
install -d %{buildroot}%{_localstatedir}/lib/%{rname}
pushd %{buildroot}%{_localstatedir}/lib/%{rname} && {
	touch %{rname}.state
	touch timestamps
popd
}

%find_lang %{rname}

%post
%_post_service %{name} %{rname}.service

%preun
%_preun_service %{name} %{rname}.service

%postun
%_postun_unit %{rname}.service 

%files -f %{rname}.lang
%doc AUTHORS CONTRIBUTING ChangeLog NEWS README TODO
%doc README.urpmi
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-avahi-autoipd.conf
%{_sysconfdir}/dbus-1/system.d/nm-dhcp-client.conf
%{_sysconfdir}/dbus-1/system.d/nm-dispatcher.conf
%{_sysconfdir}/dbus-1/system.d/nm-ifcfg-rh.conf
%dir %{_sysconfdir}/%{rname}
%config(noreplace) %{_sysconfdir}/%{rname}/NetworkManager.conf
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%dir %{_sysconfdir}/%{rname}/system-connections
%dir %{_sysconfdir}/NetworkManager/VPN
%{_bindir}/nmcli
%{_bindir}/nm-tool
%{_bindir}/nm-online
%{_sbindir}/%{rname}
%{_libexecdir}/nm-dispatcher.action
%{_libexecdir}/nm-dhcp-client.action
%{_libexecdir}/nm-avahi-autoipd.action
%dir %{_libdir}/NetworkManager
%{_libdir}/NetworkManager/*.so
%{_libdir}/pppd/*.*.*/nm-pppd-plugin.so
%dir %{_localstatedir}/run/%{rname}
%dir %{_localstatedir}/lib/%{rname}
%ghost %{_localstatedir}/lib/%{rname}/*
%{_datadir}/bash-completion/completions/nmcli
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManager.service
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/polkit-1/actions/org.freedesktop.NetworkManager.policy
/lib/udev/rules.d/*.rules
%{_systemunitdir}/NetworkManager-wait-online.service
%{_systemunitdir}/NetworkManager-dispatcher.service
%{_systemunitdir}/NetworkManager.service
%{_systemunitdir}/networkmanager.service
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files -n %{libnm_util}
%{_libdir}/libnm-util.so.%{majutil}*

%files -n %{girname}
%{_libdir}/girepository-1.0/NetworkManager-%{api}.typelib

%files -n %{devnm_util}
%dir %{_includedir}/%{rname}
%{_includedir}/%{rname}/*.h
%doc %{_datadir}/gtk-doc/html/*
%{_datadir}/gir-1.0/NetworkManager-1.0.gir
%{_libdir}/pkgconfig/%{rname}.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-util.so

%files -n %{libnm_glib}
%{_libdir}/libnm-glib.so.%{majglib}*

%files -n %{girclient}
%{_libdir}/girepository-1.0/NMClient-%{api}.typelib

%files -n %{libnm_glib_vpn}
%{_libdir}/libnm-glib-vpn.so.%{majvpn}*

%files -n %{devnm_glib}
%dir %{_includedir}/libnm-glib
%exclude %{_includedir}/libnm-glib/nm-vpn*.h
%{_includedir}/libnm-glib/*.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/libnm-glib.so
%{_datadir}/gir-1.0/NMClient-1.0.gir

%files -n %{devnm_glib_vpn}
%{_includedir}/libnm-glib/nm-vpn*.h
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/libnm-glib-vpn.so

