#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	AviSynth+ - improved version od AviSynth frameserver
Summary(pl.UTF-8):	AviSynth+ - ulepszona wersja serwera ramek AviSynth
Name:		AviSynthPlus
Version:	3.7.3
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/AviSynth/AviSynthPlus/releases
Source0:	https://github.com/AviSynth/AviSynthPlus/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e18f562c225aa04792f318a2d3039418
Patch0:		%{name}-x32.patch
URL:		https://github.com/AviSynth/AviSynthPlus
BuildRequires:	DevIL-devel
BuildRequires:	cmake >= 3.6.2
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_apidocs:BuildRequires:	sphinx-pdg-3 >= 1.3}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AviSynth+ is an improved version of the AviSynth frameserver
(<http://avisynth.nl/index.php/Main_Page>), with improved features and
developer friendliness.

%description -l pl.UTF-8
AviSynth+ to ulepszona wersja serwera ramek AviSynth
(<http://avisynth.nl/index.php/Main_Page>), o większych możliwościach
i bardziej przyjazna dla programistów.

%package devel
Summary:	Header files for AviSynthPlus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AviSynthPlus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for AviSynthPlus library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AviSynthPlus.

%package apidocs
Summary:	API documentation for AviSynthPlus library
Summary(pl.UTF-8):	Dokumentacja API biblioteki AviSynthPlus
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for AviSynthPlus library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki AviSynthPlus.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake ..

%{__make}

cd ..

%if %{with apidocs}
sphinx-build-3 -b html distrib/docs/english/source distrib/docs/english/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md distrib/Readme/readme_history.txt
%attr(755,root,root) %{_libdir}/libavisynth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavisynth.so.10
%dir %{_libdir}/avisynth
%attr(755,root,root) %{_libdir}/avisynth/libconvertstacked.so
%attr(755,root,root) %{_libdir}/avisynth/libimageseq.so
%attr(755,root,root) %{_libdir}/avisynth/libshibatch.so
%attr(755,root,root) %{_libdir}/avisynth/libtimestretch.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libavisynth.so
%{_includedir}/avisynth
%{_pkgconfigdir}/avisynth.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc distrib/docs/english/_build/html/{_images,_static,avisynthdoc,*.html,*.js}
%endif
