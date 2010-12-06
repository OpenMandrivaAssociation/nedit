Summary:	A text editor for the X Window System
Name:		nedit
Version:	5.5
Release:	%mkrel 9
License:	GPLv2+ with exception
URL:		http://www.nedit.org/
Group:		Editors
Source0:	%{name}-%{version}-src.tar.bz2
Patch0:		nedit-5.4-Makefile.patch
Patch1:		nedit-5.5-security.patch
Patch2:		nedit-5.5-utf8.patch
Patch3:		nedit-5.5-64bit-fixes.patch
Patch4: 	nedit-5.5-motif223.patch
Patch5: 	nedit-5.5-varfix.patch
Patch6: 	nedit-5.5-nc-manfix.patch
Patch7: 	nedit-5.5-visfix.patch
# Fix some string literal errors - AdamW 2008/12
Patch8:		nedit-5.5-literal.patch
BuildRequires:	byacc
BuildRequires:	libx11-devel
BuildRequires:	lesstif-devel
BuildRequires:	libxt-devel
Requires:	x11-font-adobe-100dpi
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
%patch8 -p1 -b .literal

# make it lib64 aware
perl -pi -e "s,(/usr/X11R6)/lib\b,\1/%{_lib},g" makefiles/Makefile.linux

%build
echo | %make linux OPT="%{optflags} -DBUILD_UNTESTED_NEDIT %ldflags"

%install
rm -rf %{buildroot}

(cd doc;
  mkdir -p %{buildroot}%{_mandir}/man1
  install -m 644 nedit.man %{buildroot}%{_mandir}/man1/%{name}.1
  install -m 644 nc.man %{buildroot}%{_mandir}/man1/ncl.1
)
(cd source;
  mkdir -p %{buildroot}%{_bindir}
  install -m 755 nedit %{buildroot}%{_bindir}/nedit
  install -m 755 nc %{buildroot}%{_bindir}/ncl
)

# Mandriva menu entry

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=NEdit
Comment=A text editor for the X Window System
Exec=%{_bindir}/%{name}
Icon=editors_section
Terminal=false
Type=Application
StartupNotify=true
MimeType=text/plain;
Categories=Utility;TextEditor;
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ReleaseNotes doc/nedit.doc
%{_bindir}/%{name}
%{_bindir}/ncl
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/ncl.1*
%{_datadir}/applications/mandriva-%{name}.desktop

