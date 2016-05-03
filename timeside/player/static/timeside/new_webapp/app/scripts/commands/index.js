define([
  './pool',
  '#qt_core/controllers/all',
  './dataref'
  /*'./countries',
  './allcountries'*/
],

function (pool,A,DataRefCommand) {
  'use strict';

  return pool
  	.addCommand(A.Cfg.eventApi(A.Cfg.events.init.dataRef),DataRefCommand);/*
    .addCommand('countries', countries)
    .addCommand('allcountries', allcountries);*/
});
