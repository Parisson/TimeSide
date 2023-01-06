#! /usr/bin/env bash

set -e

#[ -z $VIRTUAL_ENV ] && ( echo "You should be in a virtualenv"; false )

THISDIR=$(realpath $(dirname $0))

debs="cmake libeigen3-dev libmpg123-dev libargtable2-dev libsndfile1-dev libfftw3-dev liblapack-dev"
yaafe_git=https://github.com/Yaafe/Yaafe.git

for deb in $debs
do
  ( dpkg -l $deb | grep ^.i ) || missing_deps="$missing_deps $deb"
done
[ -z $missing_deps ] || apt-get install $missing_deps

mkdir -p $VIRTUAL_ENV/src
pushd $VIRTUAL_ENV/src

set -x

echo $yaafe_git

[ ! -d Yaafe ] && git clone $yaafe_git || true

pushd Yaafe

rm -rf build
mkdir -p build
pushd build

[ -f Makefile ] && make clean
cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=$VIRTUAL_ENV \
      -DWITH_FFTW3=ON \
      -DWITH_HDF5=OFF \
      -DWITH_LAPACK=ON \
      -DWITH_MPG123=ON \
      -DWITH_EIGEN_LIBRARY=ON \
      $* \
      ..
make
make install

popd

popd

# test package
python3 -c "import yaafelib; print (yaafelib.getYaafeVersion().decode())"

popd
