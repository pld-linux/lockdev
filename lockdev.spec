# TODO: proper group (gid 54 is rsync in PLD),
#       something with directory (/var/lock is 1771 root.uucp and belongs to FHS!)
#
Summary:	A library for locking devices
Summary(pl):	Biblioteka do blokowania urz±dzeñ
Name:		lockdev
Version:	1.0.1
Release:	0.1
License:	LGPL
Group:		Development/Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}.orig.tar.gz
Patch0:		ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}-4.1.diff.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lockdev provides a reliable way to put an exclusive lock to devices
using both FSSTND and SVr4 methods.

%description -l pl
lockdev udostêpnia wiarygodny sposób na zak³adanie wy³±cznej blokady
na urz±dzenia przy u¿yciu metod zarówno FSSTND jak i SVr4.

%package devel
Summary:	The header files for the lockdev library
Summary(pl):	Pliki nag³ówkowe biblioteki lockdev
Group:          Development/Libraries
Requires:	lockdev = %{version}-%{release}

%description devel
The lockdev library provides a reliable way to put an exclusive lock
on devices using both FSSTND and SVr4 methods. The lockdev-devel
package contains the development headers.

%description devel -l pl
Biblioteka lockdev udostêpnia wiarygodny sposób na zak³adanie
wy³±cznej blokady na urz±dzenia przy u¿yciu metod zarówno FSSTND jak i
SVr4. Ten pakiet zawiera pliki nag³ówkowe.

%package static
Summary:	Static lockdev library
Summary(pl):	Biblioteka statyczna lockdev
Group:          Development/Libraries
Requires:	lockdev-devel = %{version}-%{release}

%description static
Static lockdev library.

%description static -l pl
Biblioteka statyczna lockdev.

%prep
%setup -q
%patch0 -p1

%build
%{__make} "CFLAGS=%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
    sbindir=${RPM_BUILD_ROOT}%{_sbindir} \
    libdir=${RPM_BUILD_ROOT}%{_libdir} \
    incdir=${RPM_BUILD_ROOT}%{_includedir} \
    mandir=${RPM_BUILD_ROOT}%{_mandir}

install -d $RPM_BUILD_ROOT/var/lock

%clean
rm -fr $RPM_BUILD_ROOT

%pre
groupadd -g 54 -r -f lock

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
#%attr(2755,root,lock)	%{_sbindir}/lockdev
#%dir %attr(775,root,lock) /var/lock
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_mandir}/man*/*
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
