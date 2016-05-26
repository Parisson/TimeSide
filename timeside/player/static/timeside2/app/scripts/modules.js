define([
	'#navigation_core/index',
	'#beans/index',
	'#auth_core/index',
  '#users/index',
  '#visu/index',
  '#audio/index',
  '#data/index'
  /*'#referentiel/index',
  '#clients/index',
  '#livraison/index',
  '#communication/index',*/
  
], function (NavigationModule,BeanModule,AuthModule,UsersModule,VisuModule,AudioModule,DataModule
  /*,RefModule,ClientsModule,LivraisonModule,ComModule*/) {
  'use strict';

  return function (app) {
    app.modules.concat([
    	new NavigationModule({application : app}),
    	new BeanModule(),
    	new AuthModule(),
      new UsersModule(),
      new VisuModule(),
      new AudioModule(),
      new DataModule()
    ]);
  };
});
