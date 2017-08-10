VAMP_DIR=/usr/lib/vamp

# QM Vamp Plugins
wget https://code.soundsoftware.ac.uk/attachments/download/1602/qm-vamp-plugins-linux64-v1.7.1.tar.bz2
tar -xf qm-vamp-plugins-linux64-v1.7.1.tar.bz2
mv qm-vamp-plugins-linux64-v1.7.1/*{.cat,.n3,.so} $VAMP_DIR
rm -r qm-vamp-plugins-linux64-v1.7.1
rm qm-vamp-plugins-linux64-v1.7.1.tar.bz2

# BBC Vamp Plugins
wget https://github.com/bbc/bbc-vamp-plugins/releases/download/v1.1/Linux.64-bit.tar.gz
mkdir bbctmp
tar -xf Linux.64-bit.tar.gz -C bbctmp
mv bbctmp/*{.cat,.n3,.so} $VAMP_DIR
rm -r bbctmp
rm Linux.64-bit.tar.gz

# Chordino and NNLS Chroma
wget https://code.soundsoftware.ac.uk/attachments/download/1693/nnls-chroma-linux64-v1.1.tar.bz2
tar -xf nnls-chroma-linux64-v1.1.tar.bz2
mv nnls-chroma-linux64-v1.1/*{.cat,.n3,.so} $VAMP_DIR
rm -r nnls-chroma-linux64-v1.1
rm nnls-chroma-linux64-v1.1.tar.bz2
