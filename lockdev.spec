Summary:	A library for locking devices.
Name:		lockdev
Version:	1.0.1
Release:	1
License:	LGPL
Group:		Development/Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}.orig.tar.gz
Patch0:		ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}-4.1.diff.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lockdev provides a reliable way to put an exclusive lock to devices
using both FSSTND and SVr4 methods.

%package devel
Summary:	The header files and a static library for the lockdev library.
Group:          Development/Libraries
Requires:	lockdev = %{version}-%{release}

%description devel
The lockdev library provides a reliable way to put an exclusive lock
on devices using both FSSTND and SVr4 methods. The lockdev-devel
package contains the development headers and a static library.

%prep
%setup -q
%patch0 -p1

%build
%{__make} "CFLAGS=%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} \
    sbindir=${RPM_BUILD_ROOT}%{_sbindir} \
    libdir=${RPM_BUILD_ROOT}%{_libdir} \
    incdir=${RPM_BUILD_ROOT}%{_includedir} \
    mandir=${RPM_BUILD_ROOT}%{_mandir} \
	install
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

install -d $RPM_BUILD_ROOT/var/lock

%pre
groupadd -g 54 -r -f lock

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%attr(2755,root,lock)	%{_sbindir}/lockdev
%dir %attr(775,root,lock) /var/lock
%{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/*.a
%{_libdir}/*.so
%{_mandir}/man*/*
%{_includedir}/*
