define([
  'underscore',
  'json!#config/views.json',
  'json!#config/events.json',
  'json!#config_core/events.json',
  /*'json!#config/head.json',
  'json!#config/social.json',
  'json!#config/analytics.json',*/
  'json!#config/messages.json'


],

function (_,CfgViews,CfgEvents,CfgCoreEvents,/*CfgHead,CfgSocial,CfgAnalytics,*/CfgMessages
  ) {

  var eventsOk = _.extend(CfgEvents,CfgCoreEvents);

  return {
  	'views' : CfgViews,
    'events' : eventsOk,
    'messages' : CfgMessages,

    eventOk : function(_event) {
      return _event+':ok';
    },
    eventError : function(_event) {
      return _event+':error';
    },
    eventApi : function(_event) {
      return _event+':api';
    },
    eventApiOk : function(_event) {
      return _event+':api:ok';
    },
    eventApiError : function(_event) {
      return _event+':api:error';
    },
  };

});
