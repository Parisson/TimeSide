define([
  'underscore',
  'injector',
  'json!#config/config.json',
  'json!#config_core/api.json',
  'json!#config/api.json',
  'superapi',
  'superagent'
],

function (_,injector,config, apiConfigCore,apiConfig, superapi, superagent) {
  'use strict';

  // update baseurl
  var env = config.env;
  console.log("Okkkkk : "+env);
  var remote = config.remotes[env];


  //generating final apiConfig
  apiConfig.api.services = _.extend(apiConfigCore.api.services,apiConfig.api.services);

  var cfg = apiConfig.api;
  //cfg.baseUrls = _.clone(cfg.baseUrl);

  var cfgBaseUrl = cfg.baseUrl[env];

  //cfg.baseUrl = config.remote + cfg.baseUrl;
  cfg.baseUrl = remote + cfgBaseUrl;
  
  injector.set(injector.cfg.baseServerUrl,cfg.baseUrl)

  config.images.basepath = config.images.basepathes[env];

  var api = superapi.default(cfg);
  api.agent = superagent;

  return api;
});
