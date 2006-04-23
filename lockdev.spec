%include	/usr/lib/rpm/macros.perl
Summary:	A library for locking devices
Summary(pl):	Biblioteka do blokowania urz±dzeñ
Name:		lockdev
Version:	1.0.3
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}.orig.tar.gz
# Source0-md5:	64b9c1b87b125fc348e892e24625524a
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-baudboy.patch
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
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lockdev library.

%description static -l pl
Biblioteka statyczna lockdev.

%package baudboy
Summary:	lockdev utility
Summary(pl):	Narzêdzie lockdev
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description baudboy
This package contains sgid lockdev utility used by Baudboy API.

%description baudboy -l pl
Ten pakiet zawiera narzêdzie lockdev z ustawionym bitem sgid u¿ywane
przez API Baudboy.

%package baudboy-devel
Summary:	Baudboy interface to lockdev utility
Summary(pl):	Interfejs Baudboy do narzêdzia lockdev
Group:		Development/Libraries

%description baudboy-devel
Baudboy interface to lockdev utility.

%description baudboy-devel -l pl
Interfejs Baudboy do narzêdzia lockdev.

%package -n perl-LockDev
Summary:	LockDev - Perl extension to manage device lockfiles
Summary(pl):	LockDev - rozszerzenie Perla do zarz±dzania plikami blokuj±cymi dla urz±dzeñ
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

%description -n perl-LockDev -l pl
Metody LockDev dzia³aj± na blokadach (plikach blokuj±cych) urz±dzeñ
normalnie po³o¿onych w /var/lock. Blokada jest uzyskiwana poprzez
utworzenie pary plików po³±czonych dowi±zaniem zwyk³ym i nazwanych od
nazwy urz±dzenia (wg specyfikacji FSSTND) oraz liczby g³ównej i
pobocznej (major i minor, jak w blokadach SVr4). Pozwala to rozwi±zaæ
problem istniej±cy w przypadku u¿ywania wy³±cznie metody FSSTND, kiedy
to samo urz±dzenie istnieje pod ró¿nymi nazwami (dla wygody lub kiedy
musi byæ dostêpne dla wiêcej ni¿ jednej grupy u¿ytkowników).

Nazwy plików blokuj±cych s± zwykle w postaci LCK..ttyS1 i LCK.004.065,
a ich zawarto¶æ to identyfikator (PID) procesu posiadaj±cego blokadê.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} static \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall"

%{__make} shared lockdev \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -D_REENTRANT" \
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblockdev.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblockdev.so
%{_mandir}/man3/lockdev.3*
%{_includedir}/lockdev.h
%{_includedir}/ttylock.h

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
%{perl_vendorarch}/auto/LockDev/LockDev.bs
%attr(755,root,root) %{perl_vendorarch}/auto/LockDev/LockDev.so
%{_mandir}/man3/LockDev.3*
