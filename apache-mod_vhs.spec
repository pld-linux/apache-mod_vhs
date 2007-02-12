%define		mod_name	vhs
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Virtual Hosting
Summary(pl.UTF-8):   Moduł do Apache: wirtualny hosting
Name:		apache-mod_%{mod_name}
Version:	1.0.30
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.oav.net/projects/mod_vhs/mod_vhs-%{version}.tar.gz
# Source0-md5:	0ff70c7298e8639a00b2b0c1d90caf99
URL:		http://www.oav.net/projects/mod_vhs/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	libhome-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_vhs is an Apache 2.0 Web Server module allowing mass virtual
hosting without the need for file based configuration. The virtual
host paths are translated from a any database supported by libhome at
request time.

%description -l pl.UTF-8
mod_vhs jest modułem dla serwera Apache 2.0 dający możliwość
skonfigurowania masowego wirtualnego hostingu bez potrzeby trzymania
ustawień w plikach. Wirtualne ścieżki tłumaczone są z dowolnej bazy
wspieranej przez libhome w momencie wysłania zapytania.

%prep
%setup -q -n mod_vhs

%build
%{apxs} -c -DDEBIAN=1 mod_vhs.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README* THANKS TODO WARNING*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
