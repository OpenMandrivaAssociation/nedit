%define	name	nedit
%define	version	5.5
%define title Nedit
%define longtitle A text editor for the X Window System

Summary:	A text editor for the X Window System
Name:		%{name}
Version:	%{version}
Release:	%mkrel 5
License:	GPL
Url:		http://www.nedit.org/
Group:		Editors

Source0:	%{name}-%{version}-src.tar.bz2
Patch0:		nedit-5.4-Makefile.patch
Patch1:		nedit-5.4-security.patch
Patch2:		nedit-5.5-utf8.patch
Patch3:		nedit-5.5-64bit-fixes.patch
Patch4: nedit-5.5-motif223.patch
Patch5: nedit-5.5-varfix.patch
Patch6: nedit-5.5-nc-manfix.patch
Patch7: nedit-5.5-visfix.patch

BuildRequires:	byacc lesstif-devel >= 0.93 X11-devel xpm-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
NEdit is a multi-purpose text editor for the X Window System, which
combines a standard, easy to use, graphical user interface with the
thorough functionality and stability required by users who edit text
eighthours a day.

It provides intensive support for development in a wide variety of
languages, text processors, and other tools, but at the same time can
be used productively by just about anyone who needs to edit text.

%prep
%setup -q
%patch0 -p1 -b .Makefile
%patch1 -p1 -b .security
%patch2 -p1 -b .utf8
%patch3 -p1 -b .64bit-fixes
%patch4 -p1 -b .motif223
%patch5 -p1 -b .varfix
%patch6 -p1 -b .nc-manfix
%patch7 -p1 -b .visfix

# make it lib64 aware
perl -pi -e "s,(/usr/X11R6)/lib\b,\1/%{_lib},g" makefiles/Makefile.linux

%build
echo | %make linux OPT="$RPM_OPT_FLAGS -DBUILD_UNTESTED_NEDIT"

%install
rm -rf $RPM_BUILD_ROOT

(cd doc;
  mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
  install -m 644 nedit.man $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
  install -m 644 nc.man $RPM_BUILD_ROOT%{_mandir}/man1/ncl.1
)
(cd source;
  mkdir -p $RPM_BUILD_ROOT%{_bindir}
  install -m 755 nedit $RPM_BUILD_ROOT%{_bindir}/nedit
  install -m 755 nc $RPM_BUILD_ROOT%{_bindir}/ncl
)

# Mandriva menu entry

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/%{name}
Icon=editors_section
Terminal=false
Type=Application
StartupNotify=true
MimeType=text/plain;
Categories=Utility;TextEditor;
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ReleaseNotes doc/nedit.doc
%{_bindir}/%{name}
%{_bindir}/ncl
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/ncl.1*
%{_datadir}/applications/mandriva-%{name}.desktop
