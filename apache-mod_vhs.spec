%define		mod_name	vhs
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Virtual Hosting
Summary(pl):	Modu³ do Apache: wirtualny hosting
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
Requires(post,preun):	%{apxs}
Requires:	apache >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
mod_vhs is an Apache 2.0 Web Server module allowing mass virtual
hosting without the need for file based configuration. The virtual
host paths are translated from a any database supported by libhome at
request time.

%description -l pl
mod_vhs jest modu³em dla serwera Apache 2.0 daj±cy mo¿liwo¶æ
skonfigurowania masowego wirtualnego hostingu bez potrzeby trzymania
ustawieñ w plikach. Wirtualne ¶cie¿ki t³umaczone s± z dowolnej bazy
wspieranej przez libhome w momencie wys³ania zapytania.

%prep
%setup -q -n mod_vhs

%build
%{apxs} -c mod_vhs.c

%install
rm -rf $RPM_BUILD_ROOT

install -D .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README* THANKS TODO WARNING*
%attr(755,root,root) %{_pkglibdir}/*
