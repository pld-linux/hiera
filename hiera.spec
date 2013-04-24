#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	A simple hierarchical database supporting plugin data sources
Name:		hiera
Version:	1.0.0
Release:	1
License:	Apache v2.0
Group:		Applications/Databases
Source0:	http://downloads.puppetlabs.com/hiera/%{name}-%{version}.tar.gz
# We use a copy of misreleased 'newer' version of 1.0.0
# http://projects.puppetlabs.com/issues/16621
Source1:	%{name}.yaml
URL:		http://projects.puppetlabs.com/projects/hiera/
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	rpm-rubyprov
%if %{with tests}
BuildRequires:	ruby-mocha
BuildRequires:	ruby-rspec
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A simple hierarchical database supporting plugin data sources.

%prep
%setup -q
cp -p %{SOURCE1} hiera.yaml

%build
%if %{with tests}
ruby spec/spec_helper.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{ruby_vendorlibdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p hiera.yaml $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_var}/lib/hiera

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG LICENSE
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hiera.yaml
%attr(755,root,root) %{_bindir}/hiera
%{ruby_vendorlibdir}/hiera.rb
%{ruby_vendorlibdir}/hiera
%dir %{_var}/lib/hiera
