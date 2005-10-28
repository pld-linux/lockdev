# TODO: something with directory (/var/lock is 1771 root.uucp and belongs to FHS!)
#	either move it to subdir (but then they would be used only by this lib)
#	or change lockdev group to uucp
#	or change /var/lock gid to lock
#
%include	/usr/lib/rpm/macros.perl
Summary:	A library for locking devices
Summary(pl):	Biblioteka do blokowania urz±dzeñ
Name:		lockdev
Version:	1.0.2
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}.orig.tar.gz
# Source0-md5:	c2a9e010971ccbd642dd8e842b3a1c30
# Patch0:		ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}-5.1.diff.gz
Patch0:		%{name}-Makefile.patch
#Requires(pre):	/usr/bin/getgid
#Requires(pre):	/usr/sbin/groupadd
#Requires(postun):	/sbin/ldconfig
#Requires(postun):	/usr/sbin/groupdel
#BuildRequires:	rpmbuild(macros) >= 1.202
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

%build
%{__make} static \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall"

rm -f src/*.o
%{__make} shared \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall -D_REENTRANT" \
	LCFLAGS="%{rpmldflags}"
# don't rebuild with new .o
touch liblockdev.a

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

install -d $RPM_BUILD_ROOT/var/lock
ln -sf liblockdev.so.*.*.* $RPM_BUILD_ROOT%{_libdir}/liblockdev.so

%{__make} install -C LockDev \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%pre
%groupadd -g 34 -r -f lock
%endif

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%{nil}

#if [ "$1" = "0" ]; then
#	%userremove lock
#fi

%files
%defattr(644,root,root,755)
#%attr(2755,root,lock)	%{_sbindir}/lockdev
#%dir %attr(775,root,lock) /var/lock
%attr(755,root,root) %{_libdir}/*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_mandir}/man3/lockdev.3*
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files -n perl-LockDev
%defattr(644,root,root,755)
%{perl_vendorarch}/LockDev.pm
%dir %{perl_vendorarch}/auto/LockDev
%{perl_vendorarch}/auto/LockDev/LockDev.bs
%attr(755,root,root) %{perl_vendorarch}/auto/LockDev/LockDev.so
%{_mandir}/man3/LockDev.3*
