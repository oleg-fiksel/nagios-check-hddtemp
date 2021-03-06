# nagios-check-hddtemp
# nagios-plugin-check-hddtemp.spec

%global _unpackaged_files_terminate_build 0
%global original_name nagios-check-hddtemp
%global debug_package %{nil}

Summary: Check HDD temperature Nagios plugin
Name: nagios-plugins-check-hddtemp
Version: 0.8.2
Release: 1%{?dist}
Source0: %{original_name}-%{version}.tar.gz
License: GPLv3 or later
Group: Applications/System
BuildRequires: python-setuptools
Requires: python >= 2.6
Requires: nagios-plugins
Packager: Alexei Andrushievich <vint21h@vint21h.pp.ua>
Url: https://github.com/vint21h/nagios-check-hddtemp

%description
Check HDD temperature Nagios plugin.

%prep
%setup -n %{original_name}-%{version}

%install
mkdir -p %{buildroot}%{_libdir}/nagios/plugins
install -p -m 755 check_hddtemp.py %{buildroot}%{_libdir}/nagios/plugins/check_hddtemp

%files
%defattr(-,root,root)
%doc README.rst COPYING AUTHORS
%{_libdir}/nagios/plugins/check_hddtemp

%changelog
* Fri Jil 29 2016 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 0.8.2-1
- Update to new version

* Thu Dec 3 2015 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 0.8.1-1
- Update to new version

* Thu Dec 3 2015 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 0.8.0-1
- Update to new version

* Wed Sep 9 2015 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 0.7.0-1
- Update to new version

* Mon Jun 1 2015 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 0.6.0-1
- Update to new version

* Fri Feb 13 2015 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 0.5.7-1
- Init
