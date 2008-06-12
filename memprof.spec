%define name	memprof
%define version	0.6
%define release %mkrel 4

Summary:	Tool for memory profiling and leak detection
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source0:	http://people.redhat.com/~otaylor/memprof/%{name}-%{version}.tar.bz2
Source1:	memprof-icons.tar.bz2
Source2:	memprof-manpage.bz2
Patch:          memprof-0.6-desktopentry.patch
Patch1:		memprof-0.5.1-force-static-libbfd.patch
URL:		http://www.gnome.org/projects/memprof/
ExclusiveArch:	%{ix86}
Requires:	GConf2
BuildRequires:	libbinutils-devel, libglade2.0-devel, libgnomeui2-devel
#BuildRequires:	desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
MemProf is a tool for profiling memory usage and detecting memory
leaks. It can be used with existing binaries without need for
recompilation.

%prep
%setup -q
%patch -p1 -b .desktopentry
%patch1 -p1 -b .force-static-libbfd

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT

# needed otherwise gconf database installation will fail
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall

# man page
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

# mdk menu

#gw at the moment we patch the desktop entry directly
#desktop-file-install --vendor="" \
#  --remove-category="Application" \
#  --add-category="GTK" \
#  --add-category="X-MandrivaLinux-MoreApplications-Development-Tools" \
#  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# mdk icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
tar jxvf %{SOURCE1} -C $RPM_BUILD_ROOT%{_iconsdir}/

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/memprof/*.{a,la}

# find i18n files
%find_lang %{name}

%define schemas %{name}

%post
%if %mdkversion < 200900
%{update_menus}
%endif

%if %mdkversion < 200900
%{update_scrollkeeper}
%endif

%if %mdkversion < 200900
%post_install_gconf_schemas %{schemas}
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_scrollkeeper}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
#
%doc README AUTHORS COPYING NEWS ChangeLog 
%{_mandir}/man1/%{name}.1*
#
%{_bindir}/*
#
%dir %{_libdir}/memprof
%{_libdir}/memprof/*.so
#
%{_sysconfdir}/gconf/schemas/memprof.schemas
%{_datadir}/applications/memprof.desktop
%{_datadir}/pixmaps/memprof.png
%dir %{_datadir}/%{name}
%{_datadir}/memprof/*
#
#
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


