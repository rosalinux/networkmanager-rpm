%define	glib_name	%{name}-glib
%define	util_name	%{name}-util

%define glib_major	0
%define util_major	0

%define lib_glib_name	%mklibname %{glib_name} %{glib_major}
%define	lib_glib_dev	%mklibname -d %{glib_name}
%define lib_util_name	%mklibname %{util_name} %{util_major}
%define	lib_util_dev	%mklibname -d %{util_name}

%define	rname	NetworkManager

Summary:	%{rname}
Name:		networkmanager
Version:	0.7.0
Release:	%mkrel 0.2
Source0:	%{rname}-%{version}.tar.bz2
Patch0:		NetworkManager-0.7.0-fix-build.patch
Patch1:		NetworkManager-0.7.0-fix-undefined-reference.patch
Patch2:		NetworkManager-0.7.0-mdkconf.patch
License:	GPLv2+
Group:		System/Configuration/Networking
Url:		http://www.gnome.org/projects/NetworkManager/
BuildRequires:	libnl-devel dhcdbd wpa_supplicant libiw-devel dbus-glib-devel
BuildRequires:	perl(XML::Parser) hal-devel >= 0.5.0 nss-devel intltool
BuildRequires:	ppp-devel
Requires:	dhcdbd wpa_supplicant wireless-tools
Requires(post):	rpm-helper
Requires(preun):rpm-helper

%description
NetworkManager attempts to keep an active network connection available
at all times.  The point of NetworkManager is to make networking
configuration and setup as painless and automatic as possible.  If
using DHCP, NetworkManager is _intended_ to replace default routes,
obtain IP addresses from a DHCP server, and change nameservers
whenever it sees fit.  In effect, the goal of NetworkManager is to
make networking Just Work.

%package -n 	%{lib_glib_name}
Group:		System/Libraries
Summary:	Library for %{glib_name}

%description -n	%{lib_glib_name}
Library for %{glib_name}.

%package -n	%{lib_util_name}
Group:		System/Libraries
Summary:	Library for %{util_name}

%description -n	%{lib_util_name}
Library for %{util_name}.

%package -n	%{lib_glib_dev}
Group:		Development/C
Summary:	Devel library for %{glib_name}
Provides:	%{glib_name}-devel = %{version}-%{release}
Requires:	%{lib_glib_name} = %{version}

%description -n	%{lib_glib_dev}
Devel library for %{glib_name}.

%package -n	%{lib_util_dev}
Group:		Development/C
Summary:	Devel library for %{util_name}
Provides:	%{util_name}-devel = %{version}-%{release}
Requires:	%{lib_util_name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel

%description -n	%{lib_util_dev}
Devel library for %{util_name}.

%prep
%setup -q -n %{rname}-%{version}
%patch0 -p1 -b .buildfix
%patch1 -p1 -b .fix_undefined_reference
%patch2 -p1 -b .mandriva

%build
libtoolize --force
autoreconf -i --force
intltoolize --force
# Even though we don't require named, we still build with it
# so that if the user installs it, NM will use it automatically
%configure2_5x	--localstatedir=%{_var} \
		--disable-static \
		--with-named=%{_sbindir}/named \
		--with-named-dir=%{_var}/named/data \
		--with-named-user=named \
		--with-distro=mandriva
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{rname}

find %{buildroot} -name \*.la|xargs rm -f

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}
%_post_service %{name}dispatcher

%preun
%_preun_service %{name}dispatcher
%_preun_service %{name}

%post -n %{lib_glib_name} -p /sbin/ldconfig
%postun -n %{lib_glib_name} -p /sbin/ldconfig

%post -n %{lib_util_name} -p /sbin/ldconfig
%postun -n %{lib_util_name} -p /sbin/ldconfig


%files -f %{rname}.lang
%defattr(-,root,root)
%doc AUTHORS CONTRIBUTING ChangeLog NEWS README TODO
%{_sysconfdir}/dbus-1/system.d/NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-dhcp-client.conf
%{_initrddir}/%{name}
%{_initrddir}/%{name}dispatcher
%{_sbindir}/%{rname}
%{_sbindir}/%{rname}Dispatcher
%dir %{_sysconfdir}/%{rname}
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%{_bindir}/nm-tool
%{_libexecdir}/nm-dhcp-client.action
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*
%dir %{_var}/run/%{rname}
%{_libexecdir}/nm-crash-logger
%dir %{_datadir}/%{rname}
%{_datadir}/%{rname}/gdb-cmd


%files -n %{lib_glib_name}
%{_libdir}/libnm_glib.so.%{glib_major}*
%{_libdir}/libnm_glib_vpn.so.%{glib_major}*

%files -n %{lib_util_name}
%{_libdir}/libnm-util.so.%{util_major}*
%{_libdir}/nm-pppd-plugin.so

%files -n %{lib_glib_dev}
%dir %{_includedir}/libnm-glib
%{_includedir}/libnm-glib/*.h
%{_libdir}/libnm_glib.so
%{_libdir}/libnm_glib_vpn.so
%{_libdir}/pkgconfig/libnm_glib.pc

%files -n %{lib_util_dev}
%dir %{_includedir}/%{rname}
%{_includedir}/%{rname}/*.h
%{_libdir}/pkgconfig/%{rname}.pc
%{_libdir}/libnm-util.so
%{_libdir}/pkgconfig/libnm-util.pc

