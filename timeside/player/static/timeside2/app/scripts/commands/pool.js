define([
  'vent',
  'commando'
],

function (vent, Commando) {
  'use strict';

  return new Commando.Pool(vent);
});
