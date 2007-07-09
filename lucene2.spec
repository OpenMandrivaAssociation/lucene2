%define section         free
%define nversion        2.2.0
%define gcj_support     1

Name:           lucene2
Version:        2.2.0
Release:        %mkrel 1
Epoch:          0
Summary:        High-performance, full-featured text search engine
License:        Apache License
URL:            http://lucene.apache.org/
Group:          Development/Java
Source0:        http://apache.tradebit.com/pub/lucene/java/lucene-%{version}-src.tar.gz
Source1:        http://apache.tradebit.com/pub/lucene/java/lucene-%{version}-src.tar.gz.asc
Patch0:         lucene-2.2.0-javadoc-no-build-contrib.patch
BuildRequires:  ant
BuildRequires:  jakarta-commons-digester
BuildRequires:  javacc
BuildRequires:  java-devel
BuildRequires:  java-javadoc
BuildRequires:  jpackage-utils
BuildRequires:  jtidy
BuildRequires:  junit
BuildRequires:  zip
%if !%{gcj_support}
BuildArch:      noarch
%else
BuildRequires:  java-gcj-compat-devel
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Jakarta Lucene is a high-performance, full-featured text search engine
written entirely in Java. It is a technology suitable for nearly any
application that requires full-text search, especially cross-platform.

%package javadoc
Summary:        Javadoc for Lucene
Group:          Development/Java

%description javadoc
Javadoc for Lucene.

%package demo
Summary:        Lucene demonstrations and samples
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Lucene demonstrations and samples.

# TODO: webapp

%package src
Summary:        Source for Lucene
Group:          Development/Java

%description src
Source for Lucene.

%prep
%setup -q -n lucene-%{version}
%patch0 -p1
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}
%{__perl} -pi -e 's/<javac( |$)/<javac nowarn="true" /g' *build.xml
%{__perl} -pi -e 's/source=.*$/source="1.5"/;' build.xml

%build
mkdir -p docs
export CLASSPATH=$(build-classpath jtidy junit jakarta-commons-digester)
export OPT_JAR_LIST=:
%{ant} \
  -Djavacc.home=%{_bindir}/javacc \
  -Djavacc.jar=%{_javadir}/javacc.jar \
  -Djavacc.jar.dir=%{_javadir} \
  -Djavadoc.link=%{_javadocdir}/java \
  jar-core jar-demo javadocs

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lucene-core-%{nversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-core-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && ln -sf %{name}-core.jar %{name}.jar && ln -sf %{name}-core-%{version}.jar %{name}-%{version}.jar)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -p build/lucene-demos-%{nversion}.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-demos-%{version}.jar
ln -s %{name}-demos-%{version}.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-demos.jar

# TODO: webapp: luceneweb.war / where do we install 'em?

# src
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__tar} xOf %{SOURCE0} | zip -r $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-%{version}-src.zip -
ln -s %{name}-%{version}-src.zip $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-src.zip

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(0644,root,root,0755)
%doc CHANGES.txt LICENSE.txt README.txt
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%dir %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%dir %{_datadir}/%{name}
%exclude %{_datadir}/%{name}/*.zip
%{_datadir}/%{name}/*

# TODO: webapp

%files src
%defattr(0644,root,root,0755)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.zip


