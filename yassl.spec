# TODO
# - bundled openssl?
# - shared lib, -devel, -static
Summary:	Yet Another SSL Library
Name:		yassl
Version:	1.5.8
Release:	0.1
License:	GPL
Group:		Libraries
URL:		http://www.yassl.com/
Source0:	http://www.yassl.com/%{name}-%{version}.zip
# Source0-md5:	2f489c20fb93629ac644352d59e2c998
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
yaSSL is an SSL version 3 and TLS version 1 (client and server
supporting) C++ library. yaSSL provides a simple API and even provides
an additional OpenSSL compatibility API.

%prep
%setup -q

%build
%configure \
	%{?debug:--enable-debug} \
	--with-zlib=/usr

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/yassl
cp -a include/* $RPM_BUILD_ROOT%{_includedir}/yassl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/benchmark
%attr(755,root,root) %{_bindir}/client
%attr(755,root,root) %{_bindir}/echoclient
%attr(755,root,root) %{_bindir}/echoserver
%attr(755,root,root) %{_bindir}/server
%attr(755,root,root) %{_bindir}/test
%attr(755,root,root) %{_bindir}/testsuite
%{_includedir}/yassl
%{_libdir}/libtaocrypt.a
%{_libdir}/libyassl.a
