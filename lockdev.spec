%include	/usr/lib/rpm/macros.perl
Summary:	A library for locking devices
Summary(pl.UTF-8):	Biblioteka do blokowania urządzeń
Name:		lockdev
Version:	1.0.3
Release:	15
License:	LGPL v2.1
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}.orig.tar.gz
# Source0-md5:	64b9c1b87b125fc348e892e24625524a
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-baudboy.patch
Patch2:		%{name}-decl.patch
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	rpm-perlprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lockdev provides a reliable way to put an exclusive lock to devices
using both FSSTND and SVr4 methods.

%description -l pl.UTF-8
lockdev udostępnia wiarygodny sposób na zakładanie wyłącznej blokady
na urządzenia przy użyciu metod zarówno FSSTND jak i SVr4.

%package devel
Summary:	The header files for the lockdev library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lockdev
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The lockdev library provides a reliable way to put an exclusive lock
on devices using both FSSTND and SVr4 methods. The lockdev-devel
package contains the development headers.

%description devel -l pl.UTF-8
Biblioteka lockdev udostępnia wiarygodny sposób na zakładanie
wyłącznej blokady na urządzenia przy użyciu metod zarówno FSSTND jak i
SVr4. Ten pakiet zawiera pliki nagłówkowe.

%package static
Summary:	Static lockdev library
Summary(pl.UTF-8):	Biblioteka statyczna lockdev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lockdev library.

%description static -l pl.UTF-8
Biblioteka statyczna lockdev.

%package baudboy
Summary:	lockdev utility
Summary(pl.UTF-8):	Narzędzie lockdev
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description baudboy
This package contains sgid lockdev utility used by Baudboy API.

%description baudboy -l pl.UTF-8
Ten pakiet zawiera narzędzie lockdev z ustawionym bitem sgid używane
przez API Baudboy.

%package baudboy-devel
Summary:	Baudboy interface to lockdev utility
Summary(pl.UTF-8):	Interfejs Baudboy do narzędzia lockdev
Group:		Development/Libraries

%description baudboy-devel
Baudboy interface to lockdev utility.

%description baudboy-devel -l pl.UTF-8
Interfejs Baudboy do narzędzia lockdev.

%package -n perl-LockDev
Summary:	LockDev - Perl extension to manage device lockfiles
Summary(pl.UTF-8):	LockDev - rozszerzenie Perla do zarządzania plikami blokującymi dla urządzeń
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-LockDev
The LockDev methods act on device locks normally located in /var/lock.
The lock is acquired creating a pair of files hardlinked between them
and named after the device name (as mandated by FSSTND) and the
device's major and minor numbers (as in SVr4 locks). This permits to
circumvent a problem using only the FSSTND lock method when the same
device exists under different names (for convenience or when a device
must be accessable by more than one group of users).

The lock file names are typically in the form LCK..ttyS1 and
LCK.004.065, and their content is the pid of the process who owns the
lock.

%description -n perl-LockDev -l pl.UTF-8
Metody LockDev działają na blokadach (plikach blokujących) urządzeń
normalnie położonych w /var/lock. Blokada jest uzyskiwana poprzez
utworzenie pary plików połączonych dowiązaniem zwykłym i nazwanych od
nazwy urządzenia (wg specyfikacji FSSTND) oraz liczby głównej i
pobocznej (major i minor, jak w blokadach SVr4). Pozwala to rozwiązać
problem istniejący w przypadku używania wyłącznie metody FSSTND, kiedy
to samo urządzenie istnieje pod różnymi nazwami (dla wygody lub kiedy
musi być dostępne dla więcej niż jednej grupy użytkowników).

Nazwy plików blokujących są zwykle w postaci LCK..ttyS1 i LCK.004.065,
a ich zawartość to identyfikator (PID) procesu posiadającego blokadę.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} static \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -Wall"

%{__make} shared lockdev \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -Wall -D_REENTRANT" \
	LCFLAGS="%{rpmldflags}"

cd LockDev
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	OPTIMIZE="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	incdir=$RPM_BUILD_ROOT%{_includedir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}

%{__make} install -C LockDev \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/LockDev/.packlist

ln -sf liblockdev.so.1.0.3 $RPM_BUILD_ROOT%{_libdir}/liblockdev.so.1

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cat >$RPM_BUILD_ROOT%{_pkgconfigdir}/lockdev.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: lockdev
Description: A library for locking devices
Version: %{version}
Libs: -L${libdir} -llockdev
Cflags:
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblockdev.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblockdev.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblockdev.so
%{_mandir}/man3/lockdev.3*
%{_includedir}/lockdev.h
%{_includedir}/ttylock.h
%{_pkgconfigdir}/lockdev.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblockdev.a

%files baudboy
%defattr(644,root,root,755)
%attr(2755,root,uucp) %{_sbindir}/lockdev

%files baudboy-devel
%defattr(644,root,root,755)
%{_includedir}/baudboy.h

%files -n perl-LockDev
%defattr(644,root,root,755)
%{perl_vendorarch}/LockDev.pm
%dir %{perl_vendorarch}/auto/LockDev
%attr(755,root,root) %{perl_vendorarch}/auto/LockDev/LockDev.so
%{_mandir}/man3/LockDev.3*
