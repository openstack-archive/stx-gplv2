# build against xz?
%bcond_without xz
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb
# run internal testsuite?
%bcond_with check
# disable plugins initially
%bcond_without plugins

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define rpmhome /usr/lib/rpm

%define rpmver 4.14.0
%define srcver %{rpmver}%{?snapver:-%{snapver}}

%define bdbname libdb
%define bdbver 5.3.15
%define dbprefix db

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Group: System Environment/Base
Url: http://www.rpm.org/
Source0: %{name}-%{version}%{?snapver:-%{snapver}}.tar.bz2
%if %{with int_bdb}
Source1: db-%{bdbver}.tar.gz
%else
BuildRequires: libdb-devel
%endif

Patch1: 0001-sign-files-only.patch

# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD 
License: GPLv2+

Requires: coreutils
%if %{without int_bdb}
# db recovery tools, rpmdb_util symlinks
Requires: %{_bindir}/%{dbprefix}_stat
%endif
Requires: popt%{_isa} >= 1.10.2.1
Requires: curl

%if %{without int_bdb}
BuildRequires: %{bdbname}-devel
%endif

%if %{with check}
BuildRequires: fakechroot
%endif

# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
BuildRequires: redhat-rpm-config
BuildRequires: gawk
BuildRequires: elfutils-devel >= 0.112
BuildRequires: elfutils-libelf-devel
BuildRequires: readline-devel zlib-devel
BuildRequires: nss-devel
BuildRequires: nss-softokn-freebl-devel
# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: gettext-devel
BuildRequires: libselinux-devel
# XXX semanage is only used by sepolicy plugin but configure requires it...
BuildRequires: libsemanage-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
BuildRequires: python-devel >= 2.6
BuildRequires: lua-devel >= 5.1
BuildRequires: libcap-devel
BuildRequires: libacl-devel
%if ! %{without xz}
BuildRequires: xz-devel >= 4.999.8
%endif
%if %{with plugins}
# Required for systemd-inhibit plugin
BuildRequires: dbus-devel
%endif

# Only required by sepdebugcrcfix patch
BuildRequires: binutils-devel
# Also required as sepdebugcrcfix messes with all the make files
BuildRequires: automake

BuildRequires:    libtool
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    gettext-devel
BuildRequires:    openssl-devel
BuildRequires:    libattr-devel
BuildRequires:    nss-devel
BuildRequires:    file-devel
BuildRequires:    libarchive-devel
BuildRequires:    popt-devel
BuildRequires:    ima-evm-utils
BuildRequires:    ima-evm-utils-devel
BuildRequires:    lua-devel
BuildRequires:    zlib-devel
BuildRequires:    nspr-devel
BuildRequires:    libdb-devel


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}
Provides: librpm.so.3()(64bit) librpmio.so.3()(64bit)
Provides: librpm.so.7()(64bit) librpmio.so.7()(64bit)
# librpm uses cap_compare, introduced sometimes between libcap 2.10 and 2.16.
# A manual require is needed, see #505596
Requires: libcap%{_isa} >= 2.16

%description libs
This package contains the RPM shared libraries.

%package build-libs
Summary:  Libraries for building and signing RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires: %{_bindir}/gpg2

%description build-libs
This package contains the RPM shared libraries for building and signing
packages.

%package devel
Summary:  Development files for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires: rpm-build-libs%{_isa} = %{version}-%{release}
Requires: popt-devel%{_isa}

%description devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary: Scripts and executable programs used to build packages
Group: Development/Tools
Requires: rpm = %{version}-%{release}
Requires: elfutils >= 0.128 binutils
Requires: findutils sed grep gawk diffutils file patch >= 2.5
Requires: unzip gzip bzip2 cpio xz tar
Requires: pkgconfig >= 1:0.24
Requires: /usr/bin/gdb-add-index
# Technically rpmbuild doesn't require any external configuration, but
# creating distro-compatible packages does. To make the common case
# "just work" while allowing for alternatives, depend on a virtual
# provide, typically coming from redhat-rpm-config.
Requires: system-rpm-config
Conflicts: ocaml-runtime < 3.11.1-7

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package sign
Summary: Package signing support
Group: System Environment/Base
Requires: rpm-build-libs%{_isa} = %{version}-%{release}

%description sign
This package contains support for digitally signing RPM packages.

%package python
Summary: Python bindings for apps which will manipulate RPM packages
Group: Development/Libraries
Requires: rpm = %{version}-%{release}

%description python
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.

%package apidocs
Summary: API documentation for RPM libraries
Group: Documentation
BuildArch: noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%package cron
Summary: Create daily logs of installed packages.
Group: System Environment/Base
BuildArch: noarch
Requires: crontabs logrotate rpm = %{version}-%{release}

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.

%if %{with plugins}
%package plugin-systemd-inhibit
Summary: Rpm plugin for systemd inhibit functionality
Group: System Environment/Base
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-systemd-inhibit
%{summary}
%endif


%prep
%setup -q -n %{name}-%{srcver} %{?with_int_bdb:-a 1}

%patch1 -p1

%if %{with int_bdb}
ln -s db-%{bdbver} db
%endif

%build

# Using configure macro has some unwanted side-effects on rpm platform
# setup, use the old-fashioned way for now only defining minimal paths.
./autogen.sh \
    --prefix=%{_usr} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_var} \
    --sharedstatedir=%{_var}/lib \
    --libdir=%{_libdir} \
    %{!?with_int_bdb: --with-external-db} \
    %{!?with_plugins: --disable-plugins} \
    --with-lua \
    --with-cap \
    --with-acl \
    --enable-python \
    --with-vendor=redhat \
    --with-imaevm

make %{?_smp_mflags}
ls %{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

ln -s ./librpmio.so.7 ${RPM_BUILD_ROOT}%{_libdir}/librpmio.so.3
ln -s ./librpm.so.7 ${RPM_BUILD_ROOT}%{_libdir}/librpm.so.3
ls -l ${RPM_BUILD_ROOT}%{_libdir}

# remove all plugins except systemd_inhibit
rm -f ${RPM_BUILD_ROOT}%{_libdir}/rpm-plugins/{exec.so,sepolicy.so}

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/tmpfiles.d
echo "r /var/lib/rpm/__db.*" > ${RPM_BUILD_ROOT}/usr/lib/tmpfiles.d/rpm.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
mkdir -p $RPM_BUILD_ROOT%{rpmhome}/macros.d

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/bash-completion/completions/rpm


mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Obsoletename \
    Packages Providename Requirename Triggername Sha1header Sigmd5 \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

# plant links to relevant db utils as rpmdb_foo for documention compatibility
%if %{without int_bdb}
for dbutil in dump load recover stat upgrade verify
do
    ln -s ../../bin/%{dbprefix}_${dbutil} $RPM_BUILD_ROOT/%{rpmhome}/rpmdb_${dbutil}
done
%endif

%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.la"|xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with check}
%check
make check
[ "$(ls -A tests/rpmtests.dir)" ] && cat tests/rpmtests.log
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post build-libs -p /sbin/ldconfig
%postun build-libs -p /sbin/ldconfig

%posttrans
# XXX this is klunky and ugly, rpm itself should handle this
dbstat=/usr/lib/rpm/rpmdb_stat
if [ -x "$dbstat" ]; then
    if "$dbstat" -e -h /var/lib/rpm 2>&1 | grep -q "doesn't match library version \| Invalid argument"; then
        rm -f /var/lib/rpm/__db.* 
    fi
fi
exit 0

%files -f %{name}.lang
%defattr(-,root,root,-)

/usr/lib/tmpfiles.d/rpm.conf
%dir %{_sysconfdir}/rpm

%attr(0755, root, root) %dir /var/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/rpm/*

%{_bindir}/rpm
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm2cpio.8*

%{_datadir}/bash-completion/completions/rpm

# XXX this places translated manuals to wrong package wrt eg rpmbuild
%lang(fr) %{_mandir}/fr/man[18]/*.[18]*
%lang(ko) %{_mandir}/ko/man[18]/*.[18]*
%lang(ja) %{_mandir}/ja/man[18]/*.[18]*
%lang(pl) %{_mandir}/pl/man[18]/*.[18]*
%lang(ru) %{_mandir}/ru/man[18]/*.[18]*
%lang(sk) %{_mandir}/sk/man[18]/*.[18]*

%attr(0755, root, root) %dir %{rpmhome}
%{rpmhome}/macros
%{rpmhome}/macros.d
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc

%{rpmhome}/rpmdb_*
%{rpmhome}/rpm.daily
%{rpmhome}/rpm.log
%{rpmhome}/rpm.supp
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg

%{rpmhome}/platform

%files libs
%defattr(-,root,root)
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*

%if %{with plugins}
%files plugin-systemd-inhibit
%{_libdir}/rpm-plugins
%endif

%files build-libs
%defattr(-,root,root)
%{_libdir}/librpmbuild.so.*
%{_libdir}/librpmsign.so.*

%files build
%defattr(-,root,root)
%{_bindir}/rpmbuild
%{_bindir}/gendiff
%{_bindir}/rpmspec
%{_bindir}/rpm2archive

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*

%{rpmhome}/brp-*
%{rpmhome}/check-*
%{rpmhome}/debugedit
%{rpmhome}/sepdebugcrcfix
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/config.*
%{rpmhome}/mkinstalldirs
%{rpmhome}/macros.p*
%{rpmhome}/fileattrs

%files sign
%defattr(-,root,root)
%{_bindir}/rpmsign
%{_mandir}/man8/rpmsign.8*

%files python
%defattr(-,root,root)
%{python_sitearch}/rpm

%files devel
%defattr(-,root,root)
%{_mandir}/man8/*
%{_bindir}/rpmgraph
%{_libdir}/librp*[a-z].so
%{_libdir}/pkgconfig/rpm.pc
%{_includedir}/rpm

%files cron
%defattr(-,root,root)
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm

%files apidocs
%defattr(-,root,root)

%changelog
* Tue Jul 26 2016 Florian Festi <ffesti@redhat.com> - 4.11.3-21
- Fix --sign for rpmbuild with --quiet (#1293483)
- Adjusted fix for --noplugins option (#1264031)

* Thu Jul 14 2016 Florian Festi <ffesti@redhat.com> - 4.11.3-20
- Removed broken fix for #1293483

* Thu Apr 21 2016 Florian Festi <ffesti@redhat.com> - 4.11.3-18
- Fixed failing upstream test 257 on big endian systems (#1264463)
- Fixed problems with perl.req script (#1320214, #1275551)
- Fixed race condition in rpm file deployment when updating an existing file
  (#1320181)
- Move bdb warnings from stdin to stdout (#1297793)
- Add --justdb to the erase section of the man page, too (#1310561)
- Backport support for multi threaded xz compression (#1278924)
- Update config.guess (#1291377)
- Add --noplugins option (#1264031)
- Overwrite a file if it is not marked as config any more (#1290463)
- Add man page for systemd-inhibit plugin (#1265578)

* Tue Dec 01 2015 Pavol Babincak <pbabinca@redhat.com> - 4.11.3-17.2
- Remove one more %%{_isa} from BuildRequires (#1286805)

* Tue Dec 01 2015 Pavol Babincak <pbabinca@redhat.com> - 4.11.3-17.1
- Remove %%{_isa} from BuildRequires (#1286805)

* Fri Sep 11 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-17
- Detect plugins by DSO file name. Needed for #1160401

* Thu Aug 20 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-16
- Add fix for the fix for #1225118

* Wed Aug 19 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-15
- Remove incompatible check for multiple separators in version or release
  (#1250538)

* Wed Aug 19 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-14
- Enable plugin system but disable collection plugins. Needed for
  systemd-inhibit plugin (#1160401)
- Move systemd-inhibit plugin into its own sub packge

* Tue Jul 21 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-13
- Don't show error message if log function fails because of broken pipe
 (#1244687)

* Wed Jul 08 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-12
- Dont eat newlines on parametrized macro invocations (#1225118)

* Tue Jul 07 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-11
- Back port rpm-plugin-systemd-inhibit (#1160401)

* Thu Jul 02 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-10
- Fix stripping and debuginfo creation of binaries for changed file output.
  (#1206312)

* Tue Jun 30 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-9
- Fix color skipping of multiple files with the same content (#1170119)

* Mon Jun 29 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-8
- Add %make_build macro for hiding parallel-build magic from specs (#1221357)

* Fri Jun 26 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-7
- Add deprecation warning to description of --addsign (#1165414)

* Fri Jun 26 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-6
- Add bash completion (#1183032)

* Fri Jun 26 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-5
- Fix producing bogus dependencies by perl.req (#1191121)

* Thu Jun 25 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-4
- Clearly state that --setperms and --setugids are mutually exclusive
  (#1192000)

* Thu Jun 25 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-3
- If an error occurs during printing log message then print the error on stderr
  (#1202753)

* Thu Jun 25 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-2
- File mode from %%defattr is applied to directories with warning (#1204674)

* Fri Jun 19 2015 Florian Festi <ffesti@redhat.com> - 4.11.3-1
- Rebase to upstream release 4.11.3 (#1145970)

* Mon Jan 12 2015 Florian Festi <ffesti@redhat.com> - 4.11.1-25
- Check for malicious CPIO file name size (#1163061)
- Fixes CVE-2014-8118

* Thu Nov 13 2014 Florian Festi <ffesti@redhat.com> - 4.11.1-24
- Fix race condidition where unchecked data is exposed in the file system
  (#1163061)

* Fri Oct 10 2014 Panu matilainen <pmatilai@redhat.com> - 4.11.1-23
- Really fix brp-python-bytecompile (#1083052)

* Mon Sep 29 2014 Panu matilainen <pmatilai@redhat.com> - 4.11.1-22
- Actually apply the dirlink patch, doh.

* Mon Sep 29 2014 Panu matilainen <pmatilai@redhat.com> - 4.11.1-21
- Handle directory replaced with a symlink to one in verify (#1101861)

* Thu Sep 25 2014 Panu matilainen <pmatilai@redhat.com> - 4.11.1-20
- Byte-compile versioned python libdirs in non-root prefix too (#1083052)

* Fri Apr 25 2014 Aldy Hernandez  <aldyh@redhat.com> - 4.11.1-19
- Handle ppc64le in libtool.m4.

* Fri Apr 25 2014 Aldy Hernandez  <aldyh@redhat.com> - 4.11.1-18
- Import from rawhide:
  * Wed Jan 15 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-12
  - include ppc64le in %%power64 macro (#1052930)

* Fri Apr 25 2014 Aldy Hernandez  <aldyh@redhat.com> - 4.11.1-17
- Import from rawhide:
  * Tue Oct 01 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-8
  - add support for ppc64le architecture

* Mon Mar 24 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-16
- Fully reset file actions between rpmtsRun() calls (#1076552)

* Wed Feb 19 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-15
- Make room for SHA224 in digest bundles (#1066494)

* Tue Feb 18 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-14
- Fix incorrect header sort state on export bloating headers (#1061730)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.11.1-13
- Mass rebuild 2014-01-24

* Thu Jan 16 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-12
- Make rpm-build depend on virtual system-rpm-config provide (#1048514)

* Thu Jan 16 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-11
- Fix minidebuginfo generation on ppc64 (#1052415)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.11.1-10
- Mass rebuild 2013-12-27

* Mon Sep 30 2013 Florian Festi <ffesti@redhat.com> - 4.11.1-9
 - Fix byteorder for 64 bit tags on big endian machines (#1012946)
 - Better RPMSIGTAG_SIZE vs PMSIGTAG_LONGSIZE detection (#1012595)

* Wed Sep 11 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-8
- Fix segfault on empty -p <lua> scriptlet body (#1004062)
- Add missing dependency on tar to rpm-build (#986539)

* Thu Aug 29 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-7
- Fix relocation regression wrt unowned directories (#1001553)
- Fix build-time double-free wrt %%caps() on wildcard file entry (#1002089)
- Fix source URL in spec

* Fri Aug 02 2013 Florian Festi <ffesti@redhat.com> - 4.11.1-6
 - Disable test suite as fakechroot is not longer in the distribution

* Fri Aug 02 2013 Florian Festi <ffesti@redhat.com> - 4.11.1-5
- Revert: Clarify man page about mutually exclusive options (#969505)
- Revert: Move translated rpmgraph man pages to devel sub package (#948861)

* Thu Aug 01 2013 Florian Festi <ffesti@redhat.com> - 4.11.1-4
- Clarify man page about mutually exclusive options (#969505)
- Move translated rpmgraph man pages to devel sub package (#948861)

* Tue Jul 30 2013 Florian Festi <ffesti@redhat.com> - 4.11.1-3
- Do not filter out lib64.* dependencies (#988373)

* Fri Jul 05 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-2
- filter out non-library soname dependencies by default

* Fri Jul 05 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-1
- update to 4.11.1 (http://rpm.org/wiki/Releases/4.11.1)
- drop upstreamed patches
- fix .gnu_debuglink CRC32 after dwz, buildrequire binutils-devel (#971119)
- ensure relocatable packages always get install-prefix(es) set (#979443)

* Tue May 28 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.0.1-2
- check for stale locks when opening write-cursors (#860500, #962750...)
- serialize BDB environment open/close (#924417)

* Mon Feb 04 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.0.1-1
- update to 4.11.0.1 (http://rpm.org/wiki/Releases/4.11.0.1)

* Tue Jan 29 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.0-0.beta1.3
- revert yesterdays ghost-fix, it eats rpmdb's on upgrades

* Mon Jan 28 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.0-0.beta1.2
- armv7hl and armv7hnl should not have -mthumb (#901901)
- fix duplicate directory ownership between rpm and rpm-build (#894201)
- fix regression on paths shared between a real file/dir and a ghost

* Mon Dec 10 2012 Panu Matilainen <pmatilai@redhat.com> - 4.11.0-0.beta1.1
- update to 4.11 beta

* Mon Nov 19 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.90-0.git11989.3
- package /usr/lib/rpm/macros.d directory (related to #846679)
- fixup a bunch of old incorrect dates in spec changelog

* Sat Nov 17 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.90-0.git11989.2
- fix double-free on %caps in spec (#877512)

* Thu Nov 15 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.90-0.git11989.1
- update to 4.11 (http://rpm.org/wiki/Releases/4.11.0) post-alpha snapshot
- drop/adjust patches as necessary

* Thu Oct 11 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.1-3
- fix noarch __isa_* macro filter in installplatform (#865436)

* Wed Oct 10 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.1-2
- account for intentionally skipped files when verifying hardlinks (#864622)

* Wed Oct 03 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.1-1
- update to 4.10.1 ((http://rpm.org/wiki/Releases/4.10.1)

* Mon Jul 30 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-6
- move our tmpfiles config to more politically correct location (#840192)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-5
- force _host_vendor to redhat to better match toolchain etc (#485203)

* Thu Jun 28 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-4
- merge ppc64p7 related fixes that only went into f17 (#835978)

* Wed Jun 27 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-3
- add support for minidebuginfo generation (#834073)

* Mon Jun 25 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-2
- add dwarf compression support to debuginfo generation (#833311)

* Thu May 24 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-1
- update to 4.10.0 final

* Mon Apr 23 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-0.beta1.1
- update to 4.10.0-beta1

* Mon Apr 16 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11536.1
- newer git snapshot (#809402, #808750)
- adjust posttrans script wrt bdb string change (#803866, #805613)

* Thu Apr 05 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11519.1
- newer git snapshot to keep patch-count down
- fixes CVE-2012-0060, CVE-2012-0061 and CVE-2012-0815
- fix obsoletes in installing set getting matched on provides (#810077)

* Wed Apr 04 2012 Jindrich Novy <jnovy@redhat.com> - 4.9.90-0.git11505.12
- rebuild against new libdb

* Tue Apr 03 2012 Jindrich Novy <jnovy@redhat.com> - 4.9.90-0.git11505.11
- build with internal libdb to allow libdb build with higher soname

* Fri Mar 30 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.10
- fix base arch macro generation (#808250)

* Thu Mar 29 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.9
- accept files as command line arguments to rpmdeps again (#807767)
 
* Mon Mar 26 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.8
- remove fake library provide hacks now that deltarpm got rebuilt

* Fri Mar 23 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.7
- fix header data length calculation breakage

* Thu Mar 22 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.6
- fix keyid size bogosity causing breakage on 32bit systems

* Wed Mar 21 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.5
- add temporary fake library provides to get around deltarpm "bootstrap"
  dependency (yes its dirty)

* Wed Mar 21 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.4
- fix overzealous sanity check breaking posttrans scripts

* Tue Mar 20 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.3
- fix bad interaction with yum's test-transaction and pretrans scripts

* Tue Mar 20 2012 Jindrich Novy <jnovy@redhat.com> - 4.9.90-0.git11505.2
- rebuild

* Tue Mar 20 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.1
- update to 4.10.0 alpha (http://rpm.org/wiki/Releases/4.10.0)
- drop/adjust patches as necessary

* Wed Mar 07 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-14
- fix backport thinko in the exclude patch

* Wed Mar 07 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-13
- fix memory corruption on rpmdb size estimation (#766260)
- fix couple of memleaks in python bindings (#782147)
- fix regression in verify output formatting (#797964)
- dont process spec include in false branch of if (#782970)
- only warn on missing excluded files on build (#745629)
- dont free up file info sets on test transactions

* Thu Feb 09 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-12
- switch back to smaller BDB cache default (#752897)

* Sun Jan 15 2012 Dennis Gilmore <dennis@ausil.us> - 4.9.1.2-11
- always apply arm hfp macros, conditionally apply the logic to detect hfp

* Tue Jan 10 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-10
- adjust perl and python detection rules for libmagic change (#772699)

* Mon Jan 09 2012 Jindrich Novy <jnovy@redhat.com> - 4.9.1.2-9
- recognize perl script as perl code (#772632)

* Tue Dec 20 2011 Kay Sievers <kay@redhat.com> - 4.9.1.2-8
- add temporary rpmlib patch to support filesystem transition
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Dec 02 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-7
- switch over to libdb, aka Berkeley DB 5.x

* Thu Dec 01 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-6
- fix classification of ELF binaries with setuid/setgid bit (#758251)

* Fri Nov 25 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-5
- adjust font detection rules for libmagic change (#757105)

* Wed Nov 09 2011 Dennis Gilmore <dennis@ausil.us> - 4.9.1.2-4
- conditionally apply arm patch for hardfp on all arches but arm softfp ones

* Fri Oct 28 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-3
- adjust db util prefix & dependency due to #749293
- warn but dont fail the build if STABS encountered by debugedit (#725378)

* Wed Oct 12 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-2
- try teaching find-lang about the new gnome help layout (#736523)

* Thu Sep 29 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-1
- update to 4.9.1.2 (CVE-2011-3378)
- drop upstreamed rpmdb signal patch

* Mon Sep 19 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.1-3
- fix signal blocking/unblocking regression on rpmdb open/close (#739492)

* Mon Aug 08 2011 Adam Jackson <ajax@redhat.com> 4.9.1.1-2
- Add RPM_LD_FLAGS to build environment (#728974)

* Tue Aug 02 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.1-1
- update to 4.9.1.1

* Tue Jul 19 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1-2
- fix recursion of directories with trailing slash in file list (#722474)

* Fri Jul 15 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1-1
- update to 4.9.1 (http://rpm.org/wiki/Releases/4.9.1)
- drop no longer needed patches

* Thu Jun 16 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-10
- rebuild to fix a missing interpreter dependency due to bug #712251

* Fri Jun 10 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-9
- fix crash if prep or changelog section in spec is empty (#706959)
- fix crash on macro which undefines itself
- fix script dependency generation with file 5.07 string changes (#712251)

* Thu May 26 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-8
- add dwarf-4 support to debugedit (#707677)
- generate build-id symlinks for all filenames sharing a build-id (#641377)

* Thu Apr 07 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-7
- add missing ldconfig calls to build-libs sub-package
- fix source url

* Thu Apr 07 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-6
- revert the spec query change (#693338) for now, it breaks fedpkg

* Tue Apr 05 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-5
- verify some properties of replaced and wrong-colored files (#528383)
- only list packages that would be generated on spec query (#693338)
- preferred color packages should be erased last (#680261)
- fix leaks when freeing a populated transaction set
- take file state into account for file dependencies

* Tue Mar 22 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-4
- fix classification of elf executables with sticky bit set (#689182)

* Wed Mar 16 2011 Jindirch Novy <jnovy@redhat.com> - 4.9.0-3
- fix crash in package manifest check (#688091)

* Fri Mar 04 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-2
- fix duplicate rpmsign binary in rpm main package dragging in build-libs

* Wed Mar 02 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-1
- update to 4.9.0 final
- drop upstreamed patches

* Tue Mar 01 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.rc1.4
- spec cosmetics clean up extra whitespace + group more logically
- wipe out BDB environment at boot via tmpfiles.d

* Mon Feb 21 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.rc1.3
- fix erronous double cursor open, causing yum reinstall hang (#678644)

* Mon Feb 21 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.rc1.2
- fix broken logic in depgen collector, hopefully curing #675002

* Tue Feb 15 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.rc1.1
- update to 4.9.0-rc1
- drop upstream patches
- nss packaging has changed, buildrequire nss-softokn-freebl-devel 

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.0-0.beta1.7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.7
- fix segfault when building more than one package at a time (#675565)

* Sun Feb 06 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.6
- adjust ocaml rule for libmagic string change

* Mon Jan 31 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.5
- dont try to remove environment files if private env used (related to #671200)
- unbreak mono dependency extraction (#673663)
- complain instead of silent abort if cwd is not readable (#672576)

* Tue Jan 25 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.4
- add support for Requires(posttrans) dependencies

* Fri Jan 21 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.3
- avoid division by zero in rpmdb size calculation (#671056)
- fix secondary index iteration returing duplicate at end (#671149)
- fix rebuilddb creating duplicate indexes for first header

* Fri Jan 21 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.2
- permit queries from rpmdb on read-only media (#671200)

* Tue Jan 18 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.1
- rpm 4.9.0-beta1 (http://rpm.org/wiki/Releases/4.9.0)
  - drop no longer needed patches
  - adjust requires + buildrequires to match current needs
  - adjust rpmdb index ghosts to match the new release
  - split librpmbuild and librpmsign to a separate rpm-build-libs package
  - split rpmsign to its own package to allow signing without all the build goo
  - build-conditionalize plugins, disabled for now
  - gstreamer and printer dependency generation moving out
  - handle .so symlink dependencies with fileattrs
  - use gnupg2 for signing as that's what typically installed by default

* Tue Jan 18 2011 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-7
- bunch of spec tweaks, cleanups + corrections:
  - shorten rpm-build filelist a bit with glob use, reorder for saner grouping
  - missing isa in popt version dependency
  - only add rpmdb_foo symlinks for actually relevant db_* utils
  - drop no longer necessary file-devel dependency from rpm-devel
  - drop sqlite backend build-conditional
  - preliminaries for moving from db4 to libdb
- use gnupg2 for signing as that's more likely to be installed by default

* Mon Oct 25 2010 Jindrich Novy <jnovy@redhat.com> - 4.8.1-6
- rebuild with new xz-5.0.0

* Tue Aug 10 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-5
- create gdb index on debuginfo generation (#617166)
- rpm-build now requires /usr/bin/gdb-add-index for consistent index creation
- include COPYING in -apidocs for licensing guidelines compliance

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 02 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-3
- ugh, reversed condition braindamage in the font provide extractor "fix"

* Wed Jun 30 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-2
- fix a potential getOutputFrom() error from font provide extraction
- debug-friendlier message to aid finding other similar cases (#565223)

* Fri Jun 11 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-1
- update to 4.8.1 (http://rpm.org/wiki/Releases/4.8.1)
- drop no longer needed patches
- fix source url pointing to testing directory

* Thu Jun 03 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-19
- also strip POSIX file capabilities from hardlinks on upgrade/erase (#598775)

* Wed Jun 02 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-18
- remove s-bits on upgrade too (#598775)

* Thu May 27 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-17
- fix segfault in spec parser (#597835)

* Thu May 27 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-16
- adjust to new pkg-config behavior wrt private dependencies (#596433)
- rpm-build now requires pkgconfig >= 0.24

* Fri May 21 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-15
- handle non-existent dependency sets correctly in python (#593553)
- make find-lang look in all locale dirs (#584866)

* Fri Apr 23 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-14
- lose dangling symlink to extinct (and useless) berkeley_db_svc (#585174)

* Wed Mar 24 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-13
- fix python match iterator regression wrt boolean representation

* Wed Mar 17 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-12
- unbreak find-lang --with-man from yesterdays braindamage

* Tue Mar 16 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-11
- support single PPD providing driver for devices (#568351)
- merge the psdriver patch pile into one
- preserve empty lines in spec prep section (#573339)
- teach python bindings about RPMTRANS_FLAG_NOCONTEXTS (related to #573111)
- dont own localized man directories through find_lang (#569536)

* Mon Feb 15 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-10
- drop bogus dependency on lzma, xz is used to handle the lzma format too

* Fri Feb 05 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-9
- unbreak python(abi) requires generation (#562906)

* Fri Feb 05 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-8
- more fixes to postscript provides extractor (#562228)
- avoid accessing unrelated mount points in disk space checking (#547548)
- fix disk space checking with erasures present in transaction (#561160)

* Fri Feb 05 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-7
- couple of fixes to the postscript provides extractor (#538101)

* Thu Feb 04 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-6
- extract provides for postscript printer drivers (#538101)

* Wed Feb 03 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-5
- python byte-compilation fixes + improvements (#558997)

* Sat Jan 30 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-4
- support parallel python versions in python dependency extractor (#532118)

* Thu Jan 21 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-3
- fix segfault on failed url retrieval
- fix verification error code depending on verbosity level
- if anything in testsuite fails, dump out the log

* Fri Jan 08 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-2
- put disttag back, accidentally nuked in 4.8.0 final update

* Fri Jan 08 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-1
- update to 4.8.0 final (http://rpm.org/wiki/Releases/4.8.0)

* Thu Jan 07 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.6
- pull out macro scoping "fix" for now, it breaks font package macros

* Mon Jan 04 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.5
- always clear locally defined macros when they go out of scope

* Thu Dec 17 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.4
- permit unexpanded macros when parsing spec (#547997)

* Wed Dec 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.3
- fix a bunch of python refcount-errors causing major memory leaks

* Mon Dec 07 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.2
- fix noise from python bytecompile on non-python packages (#539635)
- make all our -devel [build]requires isa-specific
- trim out superfluous -devel dependencies from rpm-devel

* Mon Dec 07 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.1
- update to 4.8.0-beta1 (http://rpm.org/wiki/Releases/4.8.0)
- rpm-build conflicts with current ocaml-runtime

* Fri Dec 04 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.2-2
- missing error exit code from signing password checking (#496754)
- dont fail build on unrecognized data files (#532489)
- dont try to parse subkeys and secret keys (#436812)
- fix chmod test on selinux, breaking %%{_fixperms} macro (#543035)

* Wed Nov 25 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.2-1
- update to 4.7.2 (http://rpm.org/wiki/Releases/4.7.2)
- fixes #464750, #529214

* Wed Nov 18 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-10
- rebuild against BDB-4.8.24

* Wed Nov 18 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-9
- drop versioned dependency to BDB

* Wed Oct 28 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-8
- support multiple python implementations in brp-python-bytecompile (#531117)
- make disk space problem reporting a bit saner (#517418)

* Tue Oct 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-7
- fix build with BDB 4.8.x by removing XA "support" from BDB backend 
- perl dep extractor heredoc parsing improvements (#524929)

* Mon Sep 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-6
- use relative paths within db environment (related to #507309, #507309...)
- remove db environment on close in chrooted operation (related to above)
- initialize rpmlib earlier in rpm2cpio (#523260)
- fix file dependency tag extension formatting (#523282)

* Tue Sep 15 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-5
- fix duplicate dependency filtering on build (#490378)
- permit absolute paths in file lists again (#521760)
- use permissions 444 for all .debug files (#522194)
- add support for optional bugurl tag (#512774)

* Fri Aug 14 2009 Jesse Keating <jkeating@redhat.com> - 4.7.1-4
- Patch to make geode appear as i686 (#517475)

* Thu Aug 06 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-3
- rebuild because of the new xz

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-1
- update to 4.7.1 ((http://rpm.org/wiki/Releases/4.7.1)
- fix source url

* Mon Jul 20 2009 Bill Nottingham <notting@redhat.com> - 4.7.0-9
- enable XZ support

* Thu Jun 18 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-8
- updated OSGi dependency extractor (#506471)
- fix segfault in symlink fingerprinting (#505777)
- fix invalid memory access causing bogus file dependency errors (#506323)

* Tue Jun 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-7
- add dwarf-3 support to debugedit (#505774)

* Fri Jun 12 2009 Stepan Kasal <skasal@redhat.com> - 4.7.0-6
- require libcap >= 2.16 (#505596)

* Wed Jun 03 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-5
- don't mess up problem altNEVR in python ts.check() (#501068)
- fix hardlink size calculation on build (#503020)

* Thu May 14 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-4
- split cron-job into a sub-package to avoid silly deps on core rpm (#500722)
- rpm requires coreutils but not in %%post
- build with libcap and libacl
- fix pgp pubkey signature tag parsing

* Tue Apr 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-3
- couple of merge-review fixes (#226377)
  - eliminate bogus leftover rpm:rpm rpmdb ownership
  - unescaped macro in changelog
- fix find-lang --with-kde with KDE3 (#466009)
- switch back to default file digest algorithm

* Fri Apr 17 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-2
- file classification tweaks for text files (#494817)
  - disable libmagic text token checks, it's way too error-prone
  - consistently classify all text as such and include description

* Thu Apr 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-1
- update to 4.7.0 final (http://rpm.org/wiki/Releases/4.7.0)
- fixes #494049, #495429
- dont permit test-suite failure anymore

* Thu Apr 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.rc1.1
- update to 4.7.0-rc1
- fixes #493157, #493777, #493696, #491388, #487597, #493162

* Fri Apr 03 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.9
- fix recorded file state of otherwise skipped files (#492947)
- compress ChangeLog, drop old CHANGES file (#492440)

* Thu Apr  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4.7.0-0.beta1.8
- Fix sparcv9v and sparc64v targets

* Tue Mar 24 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.7
- prefer more specific types over generic "text" in classification (#491349)

* Mon Mar 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.6
- with the fd leak gone, let libmagic look into compressed files again (#491596)

* Mon Mar 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.5
- fix font provide generation on filenames with whitespace (#491597)

* Thu Mar 12 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.4
- handle RSA V4 signatures (#436812)
- add alpha arch ISA-bits
- enable internal testsuite on build

* Mon Mar 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.3
- fix _install_langs behavior (#489235)
- fix recording of file states into rpmdb on install

* Sun Mar 08 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.2
- load macros before creating directories on src.rpm install (#489104)

* Fri Mar 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.1
- update to 4.7.0-beta1 (http://rpm.org/wiki/Releases/4.7.0)

* Fri Feb 27 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-11
- build rpm itself with md5 file digests for now to ensure upgradability

* Thu Feb 26 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-10
- handle NULL passed as EVR in rpmdsSingle() again (#485616)

* Wed Feb 25 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-9
- pull out python byte-compile syntax check for now

* Mon Feb 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-8
- make -apidocs sub-package noarch
- fix source URL

* Sat Feb 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-7
- loosen up restrictions on dependency names (#455119)
- handle inter-dependent pkg-config files for requires too (#473814)
- error/warn on elf binaries in noarch package in build

* Fri Feb 20 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-6
- error out on uncompilable python code (Tim Waugh)

* Tue Feb 17 2009 Jindrich Novy <jnovy@redhat.com> - 4.6.0-5
- remove two offending hunks from anyarch patch causing that
  RPMTAG_BUILDARCHS isn't written to SRPMs

* Mon Feb 16 2009 Jindrich Novy <jnovy@redhat.com> - 4.6.0-4
- inherit group tag from the main package (#470714)
- ignore BuildArch tags for anyarch actions (#442105)
- don't check package BuildRequires when doing --rmsource (#452477)
- don't fail because of missing sources when only spec removal
  is requested (#472427)

* Mon Feb 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-3
- updated fontconfig provide script - fc-query does all the hard work now

* Mon Feb 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-2
- build against db 4.7.x

* Fri Feb 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-1
- update to 4.6.0 final
- revert libmagic looking into compressed files for now, breaks ooffice build

* Fri Feb 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.5
- enable fontconfig provides generation

* Thu Feb 05 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.4
- fixup rpm translation lookup to match Fedora specspo (#436941)

* Wed Feb 04 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.3
- extract mimehandler provides from .desktop files
- preliminaries for extracting font provides (not enabled yet)
- dont classify font metrics data as fonts
- only run script dep extraction once per file, duh

* Sat Jan 31 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.2
- change platform sharedstatedir to something more sensible (#185862)
- add rpmdb_foo links to db utils for documentation compatibility

* Fri Jan 30 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.1
- update to 4.6.0-rc4
- fixes #475582, #478907, #476737, #479869, #476201

* Fri Dec 12 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.2
- add back defaultdocdir patch which hadn't been applied on 4.6.x branch yet

* Fri Dec 12 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.1
- add dist-tag, rebuild

* Tue Dec 09 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.1
- update to rpm 4.6.0-rc3
- fixes #475214, #474550, #473239

* Wed Dec  3 2008 Jeremy Katz <katzj@redhat.com> - 4.6.0-0.rc2.9
- I built into the wrong place

* Wed Dec  3 2008 Jeremy Katz <katzj@redhat.com> - 4.6.0-0.rc2.8
- python 2.6 rebuild again

* Wed Dec 03 2008 Panu Matilainen <pmatilai@redhat.com>
- make rpm-build require pkgconfig (#473978)

* Tue Dec 02 2008 Panu Matilainen <pmatilai@redhat.com>
- fix pkg-config provide generation when pc's depend on each other (#473814)

* Mon Dec 01 2008 Jindrich Novy <jnovy@redhat.com>
- include rpmfileutil.h from rpmmacro.h, unbreaks
  net-snmp (#473420)

* Sun Nov 30 2008 Panu Matilainen <pmatilai@redhat.com>
- rebuild for python 2.6

* Sat Nov 29 2008 Panu Matilainen <pmatilai@redhat.com>
- update to 4.6.0-rc2
- fixes #471820, #473167, #469355, #468319, #472507, #247374, #426672, #444661
- enable automatic generation of pkg-config and libtool dependencies #465377

* Fri Oct 31 2008 Panu Matilainen <pmatilai@redhat.com>
- adjust find-debuginfo for "file" output change (#468129)

* Tue Oct 28 2008 Panu Matilainen <pmatilai@redhat.com>
- Florian's improved fingerprinting hash algorithm from upstream

* Sat Oct 25 2008 Panu Matilainen <pmatilai@redhat.com>
- Make noarch sub-packages actually work
- Fix defaultdocdir logic in installplatform to avoid hardwiring mandir

* Fri Oct 24 2008 Jindrich Novy <jnovy@redhat.com>
- update compat-db dependencies (#459710)

* Wed Oct 22 2008 Panu Matilainen <pmatilai@redhat.com>
- never add identical NEVRA to transaction more than once (#467822)

* Sun Oct 19 2008 Panu Matilainen <pmatilai@redhat.com>
- permit tab as macro argument separator (#467567)

* Thu Oct 16 2008 Panu Matilainen <pmatilai@redhat.com>
- update to 4.6.0-rc1 
- fixes #465586, #466597, #465409, #216221, #466503, #466009, #463447...
- avoid using %%configure macro for now, it has unwanted side-effects on rpm

* Wed Oct 01 2008 Panu Matilainen <pmatilai@redhat.com>
- update to official 4.5.90 alpha tarball 
- a big pile of misc bugfixes + translation updates
- isa-macro generation fix for ppc (#464754)
- avoid pulling in pile of perl dependencies for an unused script
- handle both "invalid argument" and clear env version mismatch on posttrans

* Thu Sep 25 2008 Jindrich Novy <jnovy@redhat.com>
- don't treat %%patch numberless if -P parameter is present (#463942)

* Thu Sep 11 2008 Panu Matilainen <pmatilai@redhat.com>
- add hack to support extracting gstreamer plugin provides (#438225)
- fix another macro argument handling regression (#461180)

* Thu Sep 11 2008 Jindrich Novy <jnovy@redhat.com>
- create directory structure for rpmbuild prior to build if it doesn't exist (#455387)
- create _topdir if it doesn't exist when installing SRPM
- don't generate broken cpio in case of hardlink pointing on softlink,
  thanks to pixel@mandriva.com

* Sat Sep 06 2008 Jindrich Novy <jnovy@redhat.com>
- fail hard if patch isn't found (#461347)

* Mon Sep 01 2008 Jindrich Novy <jnovy@redhat.com>
- fix parsing of boolean expressions in spec (#456103)
  (unbreaks pam, jpilot and maybe other builds)

* Tue Aug 26 2008 Jindrich Novy <jnovy@redhat.com>
- add support for noarch subpackages
- fix segfault in case of insufficient disk space detected (#460146)

* Wed Aug 13 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8461.2
- fix archivesize tag generation on ppc (#458817)

* Fri Aug 08 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8461.1
- new snapshot from upstream
- fixes #68290, #455972, #446202, #453364, #456708, #456103, #456321, #456913,
  #458260, #458261
- partial fix for #457360

* Thu Jul 31 2008 Florian Festi <ffesti@redhat.com>
- 4.5.90-0.git8427.1
- new snapshot from upstream

* Thu Jul 31 2008 Florian Festi <ffesti@redhat.com>
- 4.5.90-0.git8426.10
- rpm-4.5.90-posttrans.patch
- use header from rpmdb in posttrans to make anaconda happy

* Sat Jul 19 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.9
- fix regression in patch number handling (#455872)

* Tue Jul 15 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.8
- fix regression in macro argument handling (#455333)

* Mon Jul 14 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.7
- fix mono dependency extraction (adjust for libmagic string change)

* Sat Jul 12 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.6
- fix type mismatch causing funky breakage on ppc64

* Fri Jul 11 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.5
- flip back to external bdb
- fix tab vs spaces complaints from rpmlint
- add dep for lzma and require unzip instead of zip in build (#310694)
- add pkgconfig dependency to rpm-devel
- drop ISA-dependencies for initial introduction
- new snapshot from upstream for documentation fixes

* Thu Jul 10 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.4
- handle int vs external db in posttrans too

* Wed Jul 09 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.3
- require curl as external url helper

* Wed Jul 09 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.2
- add support for building with or without internal db

* Wed Jul 09 2008 Panu Matilainen <pmatilai@redhat.com>
- rpm 4.5.90-0.git8424.1 (alpha snapshot)
- adjust to build against Berkeley DB 4.5.20 from compat-db for now
- add posttrans to clean up db environment mismatch after upgrade
- forward-port devel autodeps patch

* Tue Jul 08 2008 Panu Matilainen <pmatilai@redhat.com>
- adjust for rpmdb index name change
- drop unnecessary vendor-macro patch for real
- add ISA-dependencies among rpm subpackages
- make lzma and sqlite deps conditional and disabled by default for now

* Fri Feb 01 2008 Panu Matilainen <pmatilai@redhat.com>
- spec largely rewritten, truncating changelog
