/*! wreqr.injector - v0.3.0 - 2014-05-12
 * 
 * Copyright (c) 2014 Stéphane Bachelier
 * Distributed under MIT LICENSE 
 * 
 * https://github.com/stephanebachelier/wreqr.injector
 */
(function(root, factory) {
    if(typeof exports === 'object') {
        module.exports = factory(require('backbone.wreqr'));
    }
    else if(typeof define === 'function' && define.amd) {
        define(['backbone.wreqr'], factory);
    }
    else {
        root['Wreqr.Injector'] = factory(root.Backbone.Wreqr);
    }
}(this, function(Wreqr) {

    /* global Backbone*/
    
    // Dependency injector
    // ===================
    // This module enable more decoupling by permitting to request or set a
    // resource.
    // It is built on top of `Wreqr.RequestResponse`.
    
    var Injector = (function (Wreqr) {
      'use strict';
    
      return Wreqr.RequestResponse.extend({
    
        // get
        // ---
        // Enable any component to get a resource value by passing a name
        //
        //     // di is the injector
        //     di.get('user'); // it will return the user
        get: function (name) {
          if (! this.getHandler(name)) {
            console.log('error get on '+name);
            return undefined;
          }  

          return this.getHandler(name)();
        },
    
        // set
        // ---
        // Enable any component to register a resource value by passing a name
        //
        //     // di is the injector
        //     // it will set the value user based with the name user
        //     di.set('user', user);
        set: function (name, value) {
          if (! name) {
            console.log('injector.set on undefined!');
            return this;
          }
          this.setHandler(name, function () {
            return value;
          });
          return this;
        },
    
        // req
        // ---
        // Enable any component to request a resource
        // it returns a wrapper function around `Wreqr.RequestResponse.request`,
        // that can be called at runtime.
        //
        //     // di is the injector
        //     // it return a function
        //     var func = di.req('a', 'b');
        //
        //     another example with Backbone.Model.url
        //     var model = Backbone.Model.extend({
        //       url: di.req('services', 'login');
        //     });
        req: function () {
          var args = arguments;
          var self = this;
          return function () {
            return self.request.apply(self, args);
          };
        }
      });
    })(Backbone.Wreqr);
    
    // export it
    Backbone.Wreqr.Injector = Injector;
    

    return Wreqr.Injector;

}));
