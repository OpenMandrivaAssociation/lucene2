%define section         free
%define nversion        2.3
%define gcj_support     1

Name:           lucene2
Version:        2.3.2
Release:        %mkrel 2.0.2
Epoch:          0
Summary:        High-performance, full-featured text search engine
License:        Apache License
URL:            http://lucene.apache.org/
Group:          Development/Java
Source0:        http://apache.tradebit.com/pub/lucene/java/lucene-%{version}-src.tar.gz
Source1:        http://apache.tradebit.com/pub/lucene/java/lucene-%{version}-src.tar.gz.asc
Patch0:         lucene-2.3.0-javadoc-no-build-contrib.patch
Patch1:         lucene-2.2.0-javacc-location.patch
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  javacc
BuildRequires:  java-javadoc
BuildRequires:  java-rpmbuild
BuildRequires:  zip
%if !%{gcj_support}
BuildRequires:  java-devel
BuildArch:      noarch
%else
BuildRequires:  java-gcj-compat-devel
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
%patch1 -p1
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}
%{__perl} -pi -e 's/<javac( |$)/<javac nowarn="true" /g' *build.xml
%{__perl} -pi -e 's/source=.*$/source="1.5"/;' build.xml

%build
export CLASSPATH=
export OPT_JAR_LIST="ant/ant-nodeps"
%{ant} \
  -Djavacc.home=%{_javadir} \
  -Djavacc.jar=%{_javadir}/javacc.jar \
  -Djavacc.jar.dir=%{_javadir} \
  -Djavadoc.link=%{_javadocdir}/java \
  javacc jar-core jar-demo javadocs

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a build/lucene-core-%{nversion}.jar %{buildroot}%{_javadir}/%{name}-core-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do %{__ln_s} ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
(cd %{buildroot}%{_javadir} && %{__ln_s} %{name}-core.jar %{name}.jar && %{__ln_s} %{name}-core-%{version}.jar %{name}-%{version}.jar)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a build/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}

%{__cp} -a build/lucene-demos-%{nversion}.jar \
  %{buildroot}%{_datadir}/%{name}/%{name}-demos-%{version}.jar
%{__ln_s} %{name}-demos-%{version}.jar %{buildroot}%{_datadir}/%{name}/%{name}-demos.jar

# TODO: webapp: luceneweb.war / where do we install 'em?

# src
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}

%{__tar} xOf %{SOURCE0} | zip -r %{buildroot}%{_datadir}/%{name}/%{name}-%{version}-src.zip -
%{__ln_s} %{name}-%{version}-src.zip %{buildroot}%{_datadir}/%{name}/%{name}-src.zip

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc CHANGES.txt LICENSE.txt README.txt
%{_javadir}/*
%{gcj_files}

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
