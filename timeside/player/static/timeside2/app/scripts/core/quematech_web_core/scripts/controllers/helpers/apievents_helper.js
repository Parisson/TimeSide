define([
  'vent',
  '#qt_core/controllers/config'
],

function (vent,Cfg) {
  'use strict';

  var helper = function () {
    
  };

  helper.prototype = {

    //Attention
    //Cet helper fait UN APPEL A LA FOIS!!!! Tout du moins dans sa v2 (la v1 non mais elle pétait les couilles)
    //à ré-écrire à chaque fois dans l'appelant la méthode pour faire les vent.off...



    ////////////////////////////////////////////////
    // V3
    //La v3 va créer une instance par appel, donc plusieurs appels peuvent être imbriqués (enfin!)

    //Elle garde un tableu qui est callsDoneOnHelper qui contient des objets de type :
    // {eventToLaunch : X, baseEventListened : Y, scope : OBJ}
    arrayCallsDoneHelper : [],


    listenOkErrorAndTrigger3: function(eventToLaunch,dataEvent,baseEventListened,okFunction,errorFunction,scope) {
        if (! baseEventListened)
          baseEventListened = eventToLaunch;

        //map pour conserver 

        if (! (okFunction && errorFunction))
          throw Error('APIEventsHelper : function is undefined');

        if (this.hasCallOnHelper(eventToLaunch,baseEventListened)) {
          console.error('Error : listenOkErrorAndTrigger3 called but already listened!');
        }

        var scope = this.createScopeObject(this);


        scope._realEventListened = baseEventListened; 
        scope._realOkFunc = okFunction;
        scope._realErrorFunc = errorFunction;
        scope._realScope = scope;

        scope.eventToLaunch = eventToLaunch;  //used for removing afterwards
        scope.baseEventListened = baseEventListened; //used for removing afterwards

        this.arrayCallsDoneHelper.push({baseEventListened : baseEventListened, eventToLaunch : eventToLaunch, scope : scope})


        vent.on(Cfg.eventOk(baseEventListened),scope.baseOkFunction,scope);
        vent.on(Cfg.eventError(baseEventListened),scope.baseErrorFunction,scope);
        vent.trigger(eventToLaunch,dataEvent);
    },

    //sub : create a scope object usable
    createScopeObject : function(daddy) {
      var scope = function(){};

      scope.prototype = {
        daddy : daddy,

        baseOkFunction:function(data1,data2,data3) {
          var tocall = this._realOkFunc, scope = this._realScope;
          daddy.cleanScopeObject(this);

          ( _.bind(tocall,scope) )(data1,data2,data3);
        },

        baseErrorFunction:function(error) {
          var tocall = this._realErrorFunc, scope = this._realScope;
          daddy.cleanScopeObject(this);

          ( _.bind(tocall,scope) )(error);
        }
      };

      return new scope();
    },

    //sub : called by scope objet, removes the object and the listeners on call
    cleanScopeObject : function(scope) {
      vent.off(Cfg.eventOk(scope._realEventListened),scope.baseOkFunction,scope);
      vent.off(Cfg.eventError(scope._realEventListened),scope.baseErrorFunction,scope);
      scope._realOkFunc=undefined;
      scope._realErrorFunc=undefined;
      scope._realScope=undefined;

      var mainObject = this.hasCallOnHelper(scope.eventToLaunch,scope.baseEventListened);
      if (mainObject) {
        this.arrayCallsDoneHelper = _.without(this.arrayCallsDoneHelper,mainObject);
      }
      else {
        console.error("Impossible to remove scope object!!!"+JSON.stringify(scope));
      }
    },

    //sub : test if doublon
    hasCallOnHelper : function(eventToLaunch,baseEventListened) {
      var result = _.find(this.arrayCallsDoneHelper,function(obj) {
        return obj.eventToLaunch===eventToLaunch && obj.baseEventListened === baseEventListened;
      });
      return result;
    },


     ////////////////////////////////////////////////
    // V2

    //new test
    clean_vars:function() {
      if (! this.has_vars()) {
        console.err('Error : clean_vars called but no vars!!!!');
        return;
      }

      vent.off(Cfg.eventOk(this._realEventListened),this.baseOkFunction,this);
      vent.off(Cfg.eventError(this._realEventListened),this.baseErrorFunction,this);
      this._realOkFunc=undefined;
      this._realErrorFunc=undefined;
      this._realScope=undefined;
    },

    has_vars:function() {
      return this._realOkFunc!==undefined || this._realErrorFunc!==undefined || this._realScope!==undefined; 
    },

    baseOkFunction:function(data1,data2,data3) {
      if (! this.has_vars()) {
        console.err('Error : baseOkFunction called but no vars!!!!');
        return;
      }
      var tocall = this._realOkFunc, scope = this._realScope;
      this.clean_vars();

      ( _.bind(tocall,scope) )(data1,data2,data3);
    },

    baseErrorFunction:function(error) {
      if (! this.has_vars()) {
        console.err('Error : baseErrorFunction called but no vars!!!!');
        return;
      }
      var tocall = this._realErrorFunc, scope = this._realScope;
      this.clean_vars();

      ( _.bind(tocall,scope) )(error);
    },

    listenOkErrorAndTrigger2: function(eventToLaunch,dataEvent,baseEventListened,okFunction,errorFunction,scope) {
        if (! baseEventListened)
          baseEventListened = eventToLaunch;

        if (! (okFunction && errorFunction))
          throw Error('APIEventsHelper : function is undefined');

        if (this.has_vars()) {
          console.error('Error : listenOkErrorAndTrigger2 called but already vars!!!! : '+this._realEventListened);
          this.clean_vars(); //let's be clean
        }

        this._realEventListened = baseEventListened; 
        this._realOkFunc = okFunction;
        this._realErrorFunc = errorFunction;
        this._realScope = scope;


        vent.on(Cfg.eventOk(baseEventListened),this.baseOkFunction,this);
        vent.on(Cfg.eventError(baseEventListened),this.baseErrorFunction,this);
        vent.trigger(eventToLaunch,dataEvent);
    },

    ////////////////////////////////////////////////
    // Oldie
    listenOkErrorAndTrigger: function(eventToLaunch,dataEvent,baseEventListened,okFunction,errorFunction,scope) {
        if (! baseEventListened)
          baseEventListened = eventToLaunch;

        if (! (okFunction && errorFunction))
          throw Error('APIEventsHelper : function is undefined');

        vent.on(Cfg.eventOk(baseEventListened),okFunction,scope);
        vent.on(Cfg.eventError(baseEventListened),errorFunction,scope);
        vent.trigger(eventToLaunch,dataEvent);
    },

    removeOkError:function(baseEventListened,okFunction,errorFunction,scope) {
        vent.off(Cfg.eventOk(baseEventListened),okFunction,scope);
        vent.off(Cfg.eventError(baseEventListened),errorFunction,scope);
    }
  };

  return new helper();

});
