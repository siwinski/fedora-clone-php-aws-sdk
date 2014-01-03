%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-aws-//' -e 's/-/_/g')
%global channelname pear.amazonwebservices.com

Name:           php-aws-sdk
Version:        2.5.0
Release:        3%{?dist}
Summary:        Official PHP SDK for Amazon Web Services

Group:          Development/Libraries
License:        Apache 2.0
URL:            http://pear.amazonwebservices.com/package/sdk
Source0:        http://pear.amazonwebservices.com/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires:	php-common >= 5.2
Requires:	php-pear(PEAR)
Requires:	php-channel(%{channelname})
Requires:	php-pdo
Requires:	php-reflection
Requires:	php-spl
Requires:	php-simplexml
Requires:	php-ctype
Requires:	php-curl
Requires:	php-date
Requires:	php-dom
Requires:	php-hash
Requires:	php-json
Requires:	php-libxml
Requires:	php-mbstring
Requires:	php-openssl
Requires:	php-pcre
Requires:	php-session
Requires:	php-sqlite3
Requires:	php-Monolog
Requires:       php-Monolog-dynamo
Requires:	php-symfony-yaml
Requires:	php-guzzle-Guzzle >= 3.7.0
Requires:	php-guzzle-Guzzle < 3.9.0
Provides:	php-pear(%{pear_name}) = %{version}
Provides:	php-pear(%{channelname}/%{pear_name}) = %{version}


%description
The AWS SDK for PHP enables PHP developers to easily work with Amazon Web
Services and build scalable solutions with Amazon S3, Amazon DynamoDB,
Amazon Glacier, and more.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.amazonwebservices.com/%{pear_name} >/dev/null || :
fi


%files
%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/AWSSDKforPHP/

%changelog
* Thu Jan 02 2014 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-3
- Fix file installation
* Mon Dec 30 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-2
- add php-Monolog-dynamo dependency
- update naming on dependency php-symfony-yaml
- fix max version require on guzzle dependency
* Sun Dec 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-1
- update to latest upstrean version
* Mon Nov 18 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.10-1
- update to latest upstream version
- add php-symfony2-Yaml(version2) and php-Monolog
- remove dependency php-symfony2-YAML(version1)
- set version contraint for php-guzzle-Guzzle dependency
* Mon Sep 09 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.5-2
- add guzzle dependency.
- remove aws.phar file
* Thu Sep 05 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.5-1
- Update to 2.4.5
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
* Wed May 08 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.2-5
- unbundle sfyaml
- fix requires
- mark doc in package.xml
* Wed May 01 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-4
- Add dependencies
- Add license clarification
* Tue Apr 30 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-3
- Fix Source, remove empty folder _doc 
* Mon Apr 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-2
- Fix License, Fix Description, move doc files
* Mon Apr 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-1
- initial package
