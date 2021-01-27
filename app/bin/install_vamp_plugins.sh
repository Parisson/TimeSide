VAMP_DIR=/usr/lib/vamp

# Install Vampy
#wget https://code.soundsoftware.ac.uk/hg/vampy/archive/e2bb3cf7adf1.tar.bz2
#tar -xf e2bb3cf7adf1.tar.bz2
#cd vampy-e2bb3cf7adf1
#LDFLAGS="-L/opt/miniconda/lib" make -f Makefile.linux CXXFLAGS='-DHAVE_NUMPY -O2 -Wall -Werror -fno-strict-aliasing -fPIC -I/opt/miniconda/include/python2.7 -I/opt/miniconda/lib/python2.7/site-packages/numpy/core/include/'
#make install
# Todo: install dir is /usr/local/lib/vamp and is different from $VAMP_DIR
#cd ..
#rm e2bb3cf7adf1.tar.bz2
#rm -r vampy-e2bb3cf7adf1

# Link Python vamp plugins from Timeside
#ln -s /srv/lib/timeside/timeside/plugins/analyzer/externals/vampy/* $VAMP_DIR/

# QM Vamp Plugins
wget --no-check-certificate https://code.soundsoftware.ac.uk/attachments/download/1602/qm-vamp-plugins-linux64-v1.7.1.tar.bz2
tar -xf qm-vamp-plugins-linux64-v1.7.1.tar.bz2
mv qm-vamp-plugins-linux64-v1.7.1/*{.cat,.n3,.so} $VAMP_DIR
rm -r qm-vamp-plugins-linux64-v1.7.1
rm qm-vamp-plugins-linux64-v1.7.1.tar.bz2

# BBC Vamp Plugins
wget --no-check-certificate https://github.com/bbc/bbc-vamp-plugins/releases/download/v1.1/Linux.64-bit.tar.gz
mkdir bbctmp
tar -xf Linux.64-bit.tar.gz -C bbctmp
mv bbctmp/*{.cat,.n3,.so} $VAMP_DIR
rm -r bbctmp
rm Linux.64-bit.tar.gz

# Chordino and NNLS Chroma
wget --no-check-certificate https://code.soundsoftware.ac.uk/attachments/download/1693/nnls-chroma-linux64-v1.1.tar.bz2
tar -xf nnls-chroma-linux64-v1.1.tar.bz2
mv nnls-chroma-linux64-v1.1/*{.cat,.n3,.so} $VAMP_DIR
rm -r nnls-chroma-linux64-v1.1
rm nnls-chroma-linux64-v1.1.tar.bz2
