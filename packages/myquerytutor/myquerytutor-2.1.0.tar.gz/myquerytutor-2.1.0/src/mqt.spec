 
#
# spec file for MyQueryTutor
#


Name:           MyQueryTutor
Summary:        Educational tool to teach SQL
Version:        1.1
Release:        0
License:        GPL-3.0+
Group:          Development
Url:            https://gitlab.com/tuxta/myquerytutor
Source:         %{name}-%{version}.tar.bz2
Source1:        %{name}.desktop
Patch0:         %{name}-qmessagebox.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       python3
Requires:       python-ldap >= 2.0.1
Requires:       python-qt3 >= 3.10
Requires:       python-smbpasswd
Requires:       qt5 >= 3.2.0
BuildRequires:  python
BuildRequires:  python-ldap >= 2.0.1
BuildRequires:  python-qt3 >= 3.10
BuildRequires:  python-smbpasswd
BuildRequires:  qt3 >= 3.2.0

%description
Luma is a graphical utility for accessing and managing data stored on
LDAP servers. It is written in Python, using PyQt and
python-ldap. Plugin-support is included and useful widgets with
LDAP-functionality for easy creation of plugins are delivered.

%prep
%setup -q
%patch0

%build

%install
%{__install} -d %{buildroot}%{_prefix}
%{__python} ./install.py --prefix="%{buildroot}%{_prefix}"

%{__install} -D -m0644 %{S:1} %{buildroot}%{_datadir}/applications/%{name}.desktop
%{__install} -D -m0644 share/%{name}/icons/%{name}-128.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%files
%defattr(-,root,root)
%doc LICENSE README
%{_bindir}/%{name}
/usr/lib/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
