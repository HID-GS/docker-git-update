FROM centos:7
RUN yum -y groupinstall "Development Tools" \
    && yum -y install \
              gettext-devel \
              openssl-devel \
              perl-CPAN \
              perl-devel \
              zlib-devel

