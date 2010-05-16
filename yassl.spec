#
# Conditional build:
%bcond_with	tests		# build with tests
#
Summary:	Yet Another SSL Library
Summary(pl.UTF-8):	Jeszcze jedna biblioteka SSL
Name:		yassl
Version:	1.5.8
Release:	0.2
License:	GPL
Group:		Libraries
Source0:	http://www.yassl.com/%{name}-%{version}.zip
# Source0-md5:	2f489c20fb93629ac644352d59e2c998
Source1:	http://autoconf-archive.cryp.to/check_zlib.m4
# Source1-md5:	b578aabed5797b035075512a6c9532c5
Source2:	http://autoconf-archive.cryp.to/lib_socket_nsl.m4
# Source2-md5:	d719eef6e1f279b1fa0ed3637865a31d
Source3:	http://autoconf-archive.cryp.to/acx_pthread.m4
# Source3-md5:	4be209a685bd5d8bca16f6e4fdb25dc6
Patch0:		%{name}-am.patch
URL:		http://www.yassl.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
yaSSL is an SSL version 3 and TLS version 1 (client and server
supporting) C++ library. yaSSL provides a simple API and even provides
an additional OpenSSL compatibility API.

%description -l pl.UTF-8
yaSSL to biblioteak C++ obsługująca SSL w wersji 3 i TLS w wersji 1
(dla klienta i serwera). yaSSL udostępnia proste API, a nawet
dodatkowe API dla kompatybilności z OpenSSL.

%package devel
Summary:	Header files for yaSSL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki yaSSL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for yaSSL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki yaSSL.

%package static
Summary:	Static yaSSL library
Summary(pl.UTF-8):	Statyczna biblioteka yaSSL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static yaSSL library.

%description static -l pl.UTF-8
Statyczna biblioteka yaSSL.

%prep
%setup -q

# undos the source
find '(' -name '*.am' -o -name '*.in' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%patch0 -p1
mkdir -p m4
cp -a %{SOURCE1} m4
cp -a %{SOURCE2} m4
cp -a %{SOURCE3} m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?debug:--enable-debug} \
	--with-zlib=/usr

%{__make}

%if %{with tests}
cd testsuite
./testsuite
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/yassl
cp -a include/* $RPM_BUILD_ROOT%{_includedir}/yassl

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libtaocrypt.so.*.*.*
%attr(755,root,root) %{_libdir}/libyassl.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/benchmark
%attr(755,root,root) %{_bindir}/client
%attr(755,root,root) %{_bindir}/echoclient
%attr(755,root,root) %{_bindir}/echoserver
%attr(755,root,root) %{_bindir}/server
%attr(755,root,root) %{_bindir}/test
%attr(755,root,root) %{_bindir}/testsuite
%attr(755,root,root) %{_libdir}/libtaocrypt.so
%{_libdir}/libtaocrypt.la
%attr(755,root,root) %{_libdir}/libyassl.so
%{_libdir}/libyassl.la
%{_includedir}/yassl

%files static
%defattr(644,root,root,755)
%{_libdir}/libtaocrypt.a
%{_libdir}/libyassl.a
