define([
  ''
],

/**
  Permet de parser un fichier js de config de data pour générer les commandes get/put/post/delete 
  avec les events correspondants

    Pour chaque commande, le helper a une méthode success et error par défaut
    Pour les events, on peut ne spécifier que le baseEvent (écouté, donc Api)

    Config : 
      * name : nameType
      * onReceiveData : function (used for get)
      * baseEvent : "data" //will be like "data:create:api" with create <- name if not specific event
      * commands : [
          {
            "name" : "create", //create / get / delete / edit !!!!!
            "event" : "data:create:api", //facultatif
            "apiFunctionName" : "createData" //mandatory String or function with data in
              "fakeCallbackForSuccess" : si existe, utilisée
            "callFunc" : func(){} //facultatif, default method if not
            "onSuccess" : func(){} //facultatif, default method if not
            "onError" : func(){} //facultatif, default method if not,
            "createDataBeforeCall" : func(){} //facultatif, default method if not,
                ==> Must return {data : data, dataApi : data for api parameters}!

            "urlAfterSuccess" : "/#data/list" : facultatif for default create command
            
          }
      ]

      Après instanciation, Config a été modifié de façon à avoir directement : 
      Config : 
        * commands : [
          {
            old attribs...
            
            _callFunction : function call api
            _funcSuccess:function success with this who knows Main Config as this.config 
              and command config element as this.commandConfig
            _funcError : idem  

            _eventListened
            _eventSuccess : event to throw,
            _eventError

          }
        ]  

    USE : 
      createCommands create commands & add them to commando.pool

**/
function () {
  'use strict';

  var helper = function () {
    this.grpCommands = [];
  };

  helper.prototype = {

    //called by all.js
    init:function(allController) {
      this.A = allController;
    },

    /**
      Main func to create commands with default for create/get/update/delete
    **/
    createCommands:function(objConfig) {
      var A = this.A;

      A.log.log("datacommand_helper","Creating commands on "+JSON.stringify(objConfig));
      var grpCommand = {type : objConfig.type, commands : []};
      this.creatingObjConfig = objConfig;

      A._.each(objConfig.commands,function(objCommand) {
        A.log.log("datacommandd_helper","   Creating single command : "+JSON.stringify(objCommand));
        var _command = this.createSingleCommand(objCommand);
        if ( ! _command) {
          return console.log("error creating command on : "+objCommand);
        }
        grpCommand.commands.push(_command);

        A.log.log("datacommandd_helper","   Adding on commando on event : "+_command._eventListened);
        A.injector.get('commando.pool')
          .addCommand(_command._eventListened, _command._callFunction);

      },this);

      this.grpCommands.push(grpCommand);
    },


    /**
      Sub func to create a sub command
    **/
    createSingleCommand:function(objCommand) {
      var A = this.A;

      var _eventListened = objCommand.event ? objCommand.event : 
        A.Cfg.eventApi(this.creatingObjConfig.baseEvent+':'+objCommand.name);

      var _eventSuccess = A.Cfg.eventOk(_eventListened);
      var _eventError = A.Cfg.eventError(_eventListened);

      objCommand._eventListened = _eventListened;
      objCommand._eventSuccess = _eventSuccess;
      objCommand._eventError = _eventError;

      var _scope = {config : this.creatingObjConfig, configCommand : objCommand, A : this.A};

      var _successFunction = objCommand.onSuccess;
      if (! _successFunction)  {
        A.log.log('datacommand_helper','          creating generic success func');
        var _method = this.getDefaultMethod(objCommand.name, true);
        _successFunction = _.bind(_method,_scope);
      }

      var _errorFunction = objCommand.onError;
      if (! _errorFunction) {
        A.log.log('datacommand_helper','          creating generic error func');
        var _method = this.getDefaultMethod(objCommand.name, false);
        _errorFunction = _.bind(_method,_scope);
      }

      var _callFunction = objCommand.callFunc;
      if (! _callFunction) {
        A.log.log('datacommand_helper','          creating generic call func');
        var _method = this.defaultCallApi;
        _callFunction = _.bind(_method,_scope);
      }

      A.log.log("datacommand_helper","    Command created with : "+_eventListened+','+_eventSuccess+','+_eventError
        +', functions : ['+_successFunction+","+_errorFunction,+"]");

      objCommand._successFunction = _successFunction;
      objCommand._errorFunction = _errorFunction;
      objCommand._callFunction = _callFunction;

      return objCommand;

        
    },

    ///////////////////////////////////////////////////////////////////////////////////////////////////
    // Default methods for calling api called with scope {config : objConfig, configCommand : objConfigCommand}
    defaultCallApi:function(data) {
      var A = this.A;
      A.log.log('datacommand_helper','-> CALLING for scope : '+JSON.stringify(this.configCommand));

      this.configCommand.dataLastCall = data;
      
      var apiFunctionName = _.isString(this.configCommand.apiFunctionName) ?  
        this.configCommand.apiFunctionName : this.configCommand.apiFunctionName(data);

      var apiFunction = A.injector.get('api')[apiFunctionName];/* _.isString(this.configCommand.apiFunctionName) ?  
        A.injector.get('api')[this.configCommand.apiFunctionName] : 
        A.injector.get('api')[this.configCommand.apiFunctionName(data)];*/

      var dataApi = undefined;
      if (this.configCommand.createDataBeforeCall) {
        var result = this.configCommand.createDataBeforeCall(data);
        data = result.data;
        dataApi = result.dataApi;
      }

      //fakeMode!!
      if (this.configCommand.fakeCallbackForSuccess && _.isFunction(this.configCommand.fakeCallbackForSuccess)) {
        A.log.log('datacommand_helper','-> FAKE CALLBACK! ');
        return this.configCommand._successFunction(this.configCommand.fakeCallbackForSuccess());
      }


      return apiFunction(data,dataApi)
        .on('success',this.configCommand._successFunction)
        .on('error',this.configCommand._errorFunction);
    },

    ///////////////////////////////////////////////////////////////////////////////////////////////////
    // Default methods for success / error, called with scope {config : objConfig, configCommand : objConfigCommand}

    getDefaultMethod:function(name,isSuccess) {


      if (name==="create")
        return isSuccess ? this.defaultSuccessCreateMethod : this.defaultErrorCommand;
      if (name==="edit")
        return isSuccess ? this.defaultSuccessCreateMethod : this.defaultErrorCommand; //use same as create @TOTEST
      if (name==="edit_mine")
        return isSuccess ? this.defaultSuccessCreateMethod : this.defaultErrorCommand; //use same as create @TOTEST
      if (name==="delete")
        return isSuccess ? this.defaultSuccessDeleteMethod : this.defaultErrorCommand;

      if (! isSuccess)
        return this.defaultErrorCommand;

    },

    defaultSuccessDeleteMethod:function(res) {
      var A = this.A;
      var _objConfigCommand = this.configCommand;
      A.vent.trigger(_objConfigCommand._eventSuccess);
    },

    defaultSuccessCreateMethod:function(res) {
      var A = this.A;
      A.log.log('datacommand_helper','-> SUCCESS for scope : '+JSON.stringify(this.configCommand));

      var _objConfig = this.config;
      var _objConfigCommand = this.configCommand;
      A.vent.trigger(_objConfigCommand._eventSuccess);
      if (_objConfigCommand.urlAfterSuccess) {
        if (_.isFunction(_objConfigCommand.urlAfterSuccess))
          window.location = _objConfigCommand.urlAfterSuccess(_objConfigCommand.dataLastCall);
        else
          window.location = _objConfigCommand.urlAfterSuccess;
      }
    },


    defaultErrorCommand : function(res) {
      var A = this.A;
      A.log.log('datacommand_helper','-> ERROR for scope : '+JSON.stringify(this.configCommand));

      A.vent.trigger(A.Cfg.events.ui.waiting.stop);
      var _msg="Generic error server";

      if (res.text)
        _msg = _msg+" : "+res.text;
      else
        _msg = _msg+ (res.body && res.body.error ? " ["+res.body.error+"]" : "")
            +(res.body && res.body.message ?  " ["+res.body.message+"]" : "");

      
      A.vent.trigger(A.Cfg.events.ui.notification.show,{type : 'danger', text : _msg});

      A.vent.trigger(this.configCommand._event);
    }


  };

  return new helper();

});
