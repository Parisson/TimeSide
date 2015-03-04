'use strict';

var waves = {};

// ui components
waves.ui = {
  timeline: require('timeline'),
  layer: require('layer'),
  waveform: require('waveform'),
  segment: require('segment'),
  marker: require('marker'),
  breakpoint: require('breakpoint'),
  label: require('label'),
  zoomer: require('zoomer'),
  utils: require('utils')
};

waves.loaders = require('loaders');

waves.audio = {
	audioContext: require('audio-context'),
	granularEngine: require('granular-engine'),
	metronome: require('metronome'),
	playControl: require('play-control'),
	playerEngine: require('player-engine'),
	priorityQueue: require('priority-queue'),
	scheduler: require('scheduler'),
	segmentEngine: require('segment-engine'),
	simpleScheduler: require('simple-scheduler'),
	timeEngine: require('time-engine'),
	transport: require('transport')
};

waves.lfo = {};

// expose d3;
waves.d3 = waves.ui.timeline.d3;

module.exports = waves;