#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	A simple hierarchical database supporting plugin data sources
Name:		hiera
# http://docs.puppetlabs.com/hiera/
# Hiera 3.0 is included with open source Puppet versions 4.2 and up.
# Hiera 1.0 is compatible with Puppet 3.x and is included in Puppet Enterprise 3.x.
Version:	1.3.4
Release:	1
License:	Apache v2.0
Group:		Applications/Databases
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	9d83ce8a56cf74ae93bc55ce878da9f3
# Copied from http://downloads.puppetlabs.com/hiera/%{name}-%{version}.tar.gz
# tarball ext/hiera.yaml, as ext/ dir is not included in gem, but we want gem for .gemspec
Source1:	%{name}.yaml
URL:		http://projects.puppetlabs.com/projects/hiera/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
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
install -d ext
cp -p %{SOURCE1} ext/hiera.yaml

%build
# write .gemspec
%__gem_helper spec

# why pure? just json will do
%{__sed} -i -e 's/json_pure/json/' *.gemspec

%if %{with tests}
ruby spec/spec_helper.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{ruby_vendorlibdir},%{ruby_specdir},%{_var}/lib/hiera}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p ext/hiera.yaml $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{name}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hiera.yaml
%attr(755,root,root) %{_bindir}/hiera
%{ruby_vendorlibdir}/hiera.rb
%{ruby_vendorlibdir}/hiera
%{ruby_specdir}/%{name}-%{version}.gemspec
%dir %{_var}/lib/hiera
