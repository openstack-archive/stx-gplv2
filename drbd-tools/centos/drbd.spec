# Define init script directory. %{_initddir} is available from Fedora
# 9 forward; CentOS knows 5 only %{_initrddir}. Neither are known to
# autoconf...
%{!?_initddir: %{expand: %%global _initddir %{_initrddir}}}

# Compatibility macro wrappers for legacy RPM versions that do not
# support conditional builds
%{!?bcond_without: %{expand: %%global bcond_without() %%{expand:%%%%{!?_without_%%{1}:%%%%global with_%%{1} 1}}}}
%{!?bcond_with:    %{expand: %%global bcond_with()    %%{expand:%%%%{?_with_%%{1}:%%%%global with_%%{1} 1}}}}
%{!?with:          %{expand: %%global with()          %%{expand:%%%%{?with_%%{1}:1}%%%%{!?with_%%{1}:0}}}}
%{!?without:       %{expand: %%global without()       %%{expand:%%%%{?with_%%{1}:0}%%%%{!?with_%%{1}:1}}}}

# Conditionals
# Invoke "rpmbuild --without <feature>" or "rpmbuild --with <feature>"
# to disable or enable specific features
%bcond_without udev
%bcond_without pacemaker
%bcond_with rgmanager
%bcond_without heartbeat
# conditionals may not contain "-" nor "_", hence "bashcompletion"
%bcond_without bashcompletion
# --with xen is ignored on any non-x86 architecture
%bcond_without xen
%bcond_without legacy_utils
#%ifnarch %{ix86} x86_64
%global _without_xen --without-xen
#%endif

Name: drbd
Summary: DRBD driver for Linux
Version: 8.4.3
Release: 0%{?_tis_dist}.%{tis_patch_ver}
Source: http://oss.linbit.com/%{name}/8.3/%{name}-%{version}.tar.gz

Source1: drbd.service

# WRS
Patch0001: 0001-skip_wait_con_int_on_simplex.patch
Patch0002: 0002-drbd-conditional-crm-dependency.patch
Patch0003: 0003-drbd_report_condition.patch
Patch0004: 0004-drbdadm-ipaddr-change.patch
Patch0005: 0005-drbd_reconnect_standby_standalone.patch
Patch0006: 0006-avoid-kernel-userspace-version-check.patch
Patch0007: 0007-Update-OCF-to-attempt-connect-in-certain-states.patch
Patch0008: 0008-Increase-short-cmd-timeout-to-15-secs.patch

License: GPLv2+
ExclusiveOS: linux
Group: System Environment/Kernel
URL: http://www.drbd.org/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: flex
Requires: %{name}-utils = %{version}
%if %{with udev}
Requires: %{name}-udev = %{version}
BuildRequires: udev
%endif
%if %{with pacemaker}
Requires: %{name}-pacemaker = %{version}
%endif
## %if %{with rgmanager}
## ## No.
## ## We don't want to annoy the majority of our userbase on pacemaker
## ## by pulling in the full rgmanager stack via drbd-rgmanager as well.
## Requires: %{name}-rgmanager = %{version}
## %endif
%if %{with heartbeat}
Requires: %{name}-heartbeat = %{version}
%endif
%if %{with bashcompletion}
Requires: %{name}-bash-completion = %{version}
%endif
BuildRequires: systemd-devel

%description
DRBD mirrors a block device over the network to another machine.
Think of it as networked raid 1. It is a building block for
setting up high availability (HA) clusters.

This is a virtual package, installing the full DRBD userland suite.

# Just a few docs go into the "drbd" package. Everything else is part
# of one of the drbd-* packages.
%files
%defattr(-,root,root,-)
%doc COPYING
%doc ChangeLog
%doc README

%package utils
Summary: Management utilities for DRBD
Group: System Environment/Kernel
# We used to have one monolithic userland package.
# Since all other packages require drbd-utils,
# it should be sufficient to add the conflict here.
Conflicts: drbd < 8.3.6
# These exist in centos extras:
Conflicts: drbd82 drbd83
Requires(post): chkconfig
Requires(preun): chkconfig

%description utils
DRBD mirrors a block device over the network to another machine.
Think of it as networked raid 1. It is a building block for
setting up high availability (HA) clusters.

This packages includes the DRBD administration tools.

%files utils
%defattr(755,root,root,-)
/sbin/drbdsetup
/sbin/drbdadm
/sbin/drbdmeta
%if %{with legacy_utils}
%dir /lib/drbd/
/lib/drbd/drbdsetup-83
/lib/drbd/drbdadm-83
%endif
%{_initddir}/%{name}
%attr(644,root,root) %{_unitdir}/%{name}.service
%{_sbindir}/drbd-overview
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/outdate-peer.sh
%{_prefix}/lib/%{name}/snapshot-resync-target-lvm.sh
%{_prefix}/lib/%{name}/unsnapshot-resync-target-lvm.sh
%{_prefix}/lib/%{name}/notify-out-of-sync.sh
%{_prefix}/lib/%{name}/notify-split-brain.sh
%{_prefix}/lib/%{name}/notify-emergency-reboot.sh
%{_prefix}/lib/%{name}/notify-emergency-shutdown.sh
%{_prefix}/lib/%{name}/notify-io-error.sh
%{_prefix}/lib/%{name}/notify-pri-lost-after-sb.sh
%{_prefix}/lib/%{name}/notify-pri-lost.sh
%{_prefix}/lib/%{name}/notify-pri-on-incon-degr.sh
%{_prefix}/lib/%{name}/notify.sh

%defattr(-,root,root,-)
%dir %{_var}/lib/%{name}
%config(noreplace) %attr(640, root, root) %{_sysconfdir}/drbd.conf
%dir %attr(740, root, root) %{_sysconfdir}/drbd.d
%config(noreplace) %{_sysconfdir}/drbd.d/global_common.conf
%{_mandir}/man8/drbd.8.*
%{_mandir}/man8/drbdsetup.8.*
%{_mandir}/man8/drbdadm.8.*
%{_mandir}/man5/drbd.conf.5.*
%{_mandir}/man8/drbdmeta.8.*
%doc scripts/drbd.conf.example
%doc COPYING
%doc ChangeLog
%doc README

%if %{with udev}
%package udev
Summary: udev integration scripts for DRBD
Group: System Environment/Kernel
Requires: %{name}-utils = %{version}-%{release}, udev

%description udev
This package contains udev helper scripts for DRBD, managing symlinks to
DRBD devices in /dev/drbd/by-res and /dev/drbd/by-disk.

%files udev
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/udev/rules.d/65-drbd.rules*
%endif # with udev

%if %{with pacemaker}
%package pacemaker
Summary: Pacemaker resource agent for DRBD
Group: System Environment/Base
Requires: %{name}-utils = %{version}-%{release}
License: GPLv2

%description pacemaker
This package contains the master/slave DRBD resource agent for the
Pacemaker High Availability cluster manager.

%files pacemaker
%defattr(755,root,root,-)
%{_prefix}/lib/%{name}/crm-fence-peer.sh
%{_prefix}/lib/%{name}/crm-unfence-peer.sh
%{_prefix}/lib/%{name}/stonith_admin-fence-peer.sh
%{_prefix}/lib/ocf/resource.d/linbit/drbd
%endif # with pacemaker

# Dependencies for drbd-rgmanager are particularly awful. On RHEL 5
# and prior (and corresponding Fedora releases), %{_datadir}/cluster
# was owned by rgmanager version 2, so we have to depend on that.
#
# With Red Hat Cluster 3.0.1 (around Fedora 12), the DRBD resource
# agent was merged in, and it became part of the resource-agents 3
# package (which of course is different from resource-agents on all
# other platforms -- go figure). So for resource-agents >= 3, we must
# generally conflict.
#
# Then for RHEL 6, Red Hat in all their glory decided to keep the
# packaging scheme, but kicked DRBD out of the resource-agents
# package. Thus, for RHEL 6 specifically, we must not conflict with
# resource-agents >=3, but instead require it.
#
# The saga continues:
# In RHEL 6.1 they have listed the drbd resource agent as valid agent,
# but do not include it in their resource-agents package. -> So we
# drop any dependency regarding rgmanager's version.
#
# All of this for exactly two (2) files.
%if %{with rgmanager}
%package rgmanager
Summary: Red Hat Cluster Suite agent for DRBD
Group: System Environment/Base
Requires: %{name}-utils = %{version}-%{release}

%description rgmanager
This package contains the DRBD resource agent for the Red Hat Cluster Suite
resource manager.

As of Red Hat Cluster Suite 3.0.1, the DRBD resource agent is included
in the Cluster distribution.

%files rgmanager
%defattr(755,root,root,-)
%{_datadir}/cluster/drbd.sh
%{_prefix}/lib/%{name}/rhcs_fence

%defattr(-,root,root,-)
%{_datadir}/cluster/drbd.metadata
%endif # with rgmanager

%if %{with heartbeat}
%package heartbeat
Summary: Heartbeat resource agent for DRBD
Group: System Environment/Base
Requires: %{name}-utils = %{version}-%{release}
License: GPLv2

%description heartbeat
This package contains the DRBD resource agents for the Heartbeat cluster
resource manager (in v1 compatibility mode).

%files heartbeat
%defattr(755,root,root,-)
%{_sysconfdir}/ha.d/resource.d/drbddisk
%{_sysconfdir}/ha.d/resource.d/drbdupper

%defattr(-,root,root,-)
%{_mandir}/man8/drbddisk.8.*
%endif # with heartbeat

%if %{with bashcompletion}
%package bash-completion
Summary: Programmable bash completion support for drbdadm
Group: System Environment/Base
Requires: %{name}-utils = %{version}-%{release}

%description bash-completion
This package contains programmable bash completion support for the drbdadm
management utility.

%files bash-completion
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/bash_completion.d/drbdadm*
%endif # with bashcompletion


%prep
%setup -q
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1

%build
%configure \
    --with-utils \
    --without-km \
    %{?_without_udev} \
    %{?_without_xen} \
    %{?_without_pacemaker} \
    %{?_without_heartbeat} \
    %{?_with_rgmanager} \
    %{?_without_bashcompletion} \
    %{?_without_legacy_utils} \
    --with-initdir=%{_initddir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 -p -D %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%clean
rm -rf %{buildroot}

%post utils
chkconfig --add drbd
%if %{without udev}
for i in `seq 0 15` ; do
    test -b /dev/drbd$i || mknod -m 0660 /dev/drbd$i b 147 $i;
done
%endif #without udev

%preun utils
if [ $1 -eq 0 ]; then
        %{_initrddir}/drbd stop >/dev/null 2>&1
        /sbin/chkconfig --del drbd
fi


%changelog
* Tue Feb  5 2013 Philipp Reisner <phil@linbit.com> - 8.4.3-1
- New upstream release.

* Thu Sep  6 2012 Philipp Reisner <phil@linbit.com> - 8.4.2-1
- New upstream release.

* Tue Feb 21 2012 Lars Ellenberg <lars@linbit.com> - 8.4.1-2
- Build fix for RHEL 6 and ubuntu lucid

* Tue Dec 20 2011 Philipp Reisner <phil@linbit.com> - 8.4.1-1
- New upstream release.

* Wed Jul 15 2011 Philipp Reisner <phil@linbit.com> - 8.4.0-1
- New upstream release.

* Fri Jan 28 2011 Philipp Reisner <phil@linbit.com> - 8.3.10-1
- New upstream release.

* Fri Oct 22 2010 Philipp Reisner <phil@linbit.com> - 8.3.9-1
- New upstream release.

* Wed Jun  2 2010 Philipp Reisner <phil@linbit.com> - 8.3.8-1
- New upstream release.

* Thu Jan 13 2010 Philipp Reisner <phil@linbit.com> - 8.3.7-1
- New upstream release.

* Thu Nov  8 2009 Philipp Reisner <phil@linbit.com> - 8.3.6-1
- New upstream release.

* Thu Oct 27 2009 Philipp Reisner <phil@linbit.com> - 8.3.5-1
- New upstream release.

* Wed Oct 21 2009 Florian Haas <florian@linbit.com> - 8.3.4-12
- Packaging makeover.

* Thu Oct  6 2009 Philipp Reisner <phil@linbit.com> - 8.3.4-1
- New upstream release.

* Thu Oct  5 2009 Philipp Reisner <phil@linbit.com> - 8.3.3-1
- New upstream release.

* Fri Jul  3 2009 Philipp Reisner <phil@linbit.com> - 8.3.2-1
- New upstream release.

* Fri Mar 27 2009 Philipp Reisner <phil@linbit.com> - 8.3.1-1
- New upstream release.

* Thu Dec 18 2008 Philipp Reisner <phil@linbit.com> - 8.3.0-1
- New upstream release.

* Thu Nov 12 2008 Philipp Reisner <phil@linbit.com> - 8.2.7-1
- New upstream release.

* Fri May 30 2008 Philipp Reisner <phil@linbit.com> - 8.2.6-1
- New upstream release.

* Tue Feb 12 2008 Philipp Reisner <phil@linbit.com> - 8.2.5-1
- New upstream release.

* Fri Jan 11 2008 Philipp Reisner <phil@linbit.com> - 8.2.4-1
- New upstream release.

* Wed Jan  9 2008 Philipp Reisner <phil@linbit.com> - 8.2.3-1
- New upstream release.

* Fri Nov  2 2007 Philipp Reisner <phil@linbit.com> - 8.2.1-1
- New upstream release.

* Fri Sep 28 2007 Philipp Reisner <phil@linbit.com> - 8.2.0-1
- New upstream release.

* Mon Sep  3 2007 Philipp Reisner <phil@linbit.com> - 8.0.6-1
- New upstream release.

* Fri Aug  3 2007 Philipp Reisner <phil@linbit.com> - 8.0.5-1
- New upstream release.

* Wed Jun 27 2007 Philipp Reisner <phil@linbit.com> - 8.0.4-1
- New upstream release.

* Mon May 7 2007 Philipp Reisner <phil@linbit.com> - 8.0.3-1
- New upstream release.

* Fri Apr 6 2007 Philipp Reisner <phil@linbit.com> - 8.0.2-1
- New upstream release.

* Mon Mar 3 2007 Philipp Reisner <phil@linbit.com> - 8.0.1-1
- New upstream release.

* Wed Jan 24 2007 Philipp Reisner <phil@linbit.com>  - 8.0.0-1
- New upstream release.

