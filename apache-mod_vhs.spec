# TODO
# - fix build with apache 2.2 (regex_t)
%define		mod_name	vhs
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Virtual Hosting
Summary(pl):	Modu� do Apache: wirtualny hosting
Name:		apache-mod_%{mod_name}
Version:	1.0.26
Release:	0.1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.oav.net/projects/mod_vhs/mod_vhs-%{version}.tar.gz
# Source0-md5:	deb33f6104ca5453ec16a7056d44cc0b
URL:		http://www.oav.net/projects/mod_vhs/
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	%{apxs}
BuildRequires:	libhome-devel
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_vhs is an Apache 2.0 Web Server module allowing mass virtual
hosting without the need for file based configuration. The virtual
host paths are translated from a any database supported by libhome at
request time.

%description -l pl
mod_vhs jest modu�em dla serwera Apache 2.0 daj�cy mo�liwo��
skonfigurowania masowego wirtualnego hostingu bez potrzeby trzymania
ustawie� w plikach. Wirtualne �cie�ki t�umaczone s� z dowolnej bazy
wspieranej przez libhome w momencie wys�ania zapytania.

%prep
%setup -q -n mod_vhs

%build
%{apxs} -c mod_vhs.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README* THANKS TODO WARNING*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
