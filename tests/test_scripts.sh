#!/bin/bash
set -e


export TEMPDIR=$(mktemp -d)
export WAVFILE=$(python -c"from timeside.core.tools.test_samples import samples; print samples['C4_scale.wav']")
export  WAVDIR=$(python -c"from timeside.core.tools.test_samples import samples; import os;print os.path.dirname(samples['C4_scale.wav'])")

echo '-----------------------------------------------------'
echo ' timeside-launch ' 
echo '-----------------------------------------------------'

timeside-launch -h
timeside-launch -C bin/presets/draw_waveform_contour_white.ts $WAVFILE -o $TEMPDIR -R 'json','yaml','xml','hdf5' -v
timeside-launch -C bin/presets/transcode_media.ts $WAVFILE -o $TEMPDIR -R 'json','yaml','xml','hdf5' -v
timeside-launch -C bin/presets/extract_aubio_bpm.ts $WAVFILE -o $TEMPDIR -R 'json','yaml','xml','hdf5' -v

echo '-----------------------------------------------------'
echo ' timeside-waveforms ' 
echo '-----------------------------------------------------'

timeside-waveforms $WAVDIR $TEMPDIR
ls $TEMPDIR
