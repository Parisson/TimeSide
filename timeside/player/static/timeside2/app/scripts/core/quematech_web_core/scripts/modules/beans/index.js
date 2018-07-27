define([
  './controllers/beans',
  './beans',
  'injector'
],

function (BeansController, beans,injector) {
  'use strict';

  return function (options) {
  
    /*injector.set(injector.config.questionslocator,new QuestionsLocator());
    var ql = injector.get(injector.config.questionslocator);*/
  	

    this.controller = new BeansController({
      beans: options ? options.beans : beans/*,
      questionsLocator : ql*/
    });
  };

});
