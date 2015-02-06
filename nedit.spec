Summary:	A text editor for the X Window System
Name:		nedit
Version:	5.5
Release:	11
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
BuildRequires:	pkgconfig(x11)
BuildRequires:	lesstif-devel
BuildRequires:	pkgconfig(xt)
Requires:	x11-font-adobe-100dpi

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



%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 5.5-9mdv2011.0
+ Revision: 613006
- the mass rebuild of 2010.1 packages

* Fri Apr 30 2010 Funda Wang <fwang@mandriva.org> 5.5-8mdv2010.1
+ Revision: 541224
- build with correct BRs

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Dec 21 2008 Adam Williamson <awilliamson@mandriva.org> 5.5-7mdv2009.1
+ Revision: 316923
- rebuild
- new license policy
- small cleanups
- add literal.patch to fix string literal issues
- rediff security.patch

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Jan 28 2008 Adam Williamson <awilliamson@mandriva.org> 5.5-6mdv2008.1
+ Revision: 159380
- requires x11-font-adobe-100dpi (#34665)
- restore spec (tv's last commit somehow left it completely empty)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel
    - do not harcode icon extension
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Jul 19 2007 Adam Williamson <awilliamson@mandriva.org> 5.5-5mdv2008.0
+ Revision: 53641
- oops, drop menu entry from file list
- rebuild with new lesstif
- drop old menu and X-Mandriva category


* Fri Mar 02 2007 Jérôme Soyer <saispo@mandriva.org> 5.5-4mdv2007.0
+ Revision: 130949
- Fix menu entry

  + Olivier Thauvin <nanardon@mandriva.org>
    - fallback to lesstif to not break cross media requirement
    - xdg menu

* Wed Feb 21 2007 Jérôme Soyer <saispo@mandriva.org> 5.5-3mdv2007.1
+ Revision: 123196
- Fix bug #28760
- Import nedit

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 5.5-2mdk
- Rebuild

* Thu Feb 24 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.5-1mdk
- 5.5
- some 64-bit fixes, though x86_64 was not affected

* Sat Aug 21 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.4-2mdk
- fix typo in menu entry

* Thu Jul 29 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 5.4-1mdk
- 5.4
- sync with fedora patches

