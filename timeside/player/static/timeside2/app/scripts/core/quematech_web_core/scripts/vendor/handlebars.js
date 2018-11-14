define([
  'handlebars.runtime',
  'json!#config/config.json',
  'injector',
  'underscore',
  'jquery',
  '#qt_core/controllers/config',
  'text!#qt_core/config/assets/svg/arrow-bottom.svg',
  'text!#qt_core/config/assets/svg/close.svg',
  'text!#qt_core/config/assets/svg/etc.svg',
  'text!#qt_core/config/assets/svg/loop.svg',
  'text!#qt_core/config/assets/svg/play.svg',
  'text!#qt_core/config/assets/svg/stop.svg',
  'text!#qt_core/config/assets/svg/volume.svg',
  'text!#qt_core/config/assets/svg/settings.svg',
  'text!#qt_core/config/assets/svg/add.svg'
],

function (Handlebars, config, injector, _,$,CfgClient, 
  arrowBottom,close, etc, loop, play, stop, volume,settings,add) {
  
  'use strict';


  ///////////////////////////////////////////////////////////////////////////
  //Creating input for free parameters
  Handlebars.registerHelper('timeside_parameter', function hop(property, context) {
    var toReturn='';
    switch (property.type) {
      case 'number' : 
        toReturn = '<input data-layout="edit_param" data-element="input" data-type="'+property.type+'" data-name="'+property.name+'" value="'+property.default+'" />';
        break;
      default : 
        break;
    }
    return toReturn;
  });
  
  ///////////////////////////////////////////////////////////////////////////
  //SPRITE HERE TEMP
  Handlebars.registerHelper('sprite', function sprite(context, spriteCode) {
    var toReturn = '';
    //console.log(spriteCode);
    switch (spriteCode) { 
      case 'arrow-bottom' :
        toReturn = _.template(arrowBottom)();
        break;
      case 'settings' :
        toReturn = _.template(settings)();
        break;
      case 'close' :
        toReturn = _.template(close)();
        break;
      case 'etc' :
        toReturn = _.template(etc)();
        break;
      case 'loop' :
        toReturn = _.template(loop)();
        break;
      case 'play' :
        toReturn = _.template(play)();
        break;
      case 'stop' :
        toReturn = _.template(stop)();
        break;
      case 'volume' :
        toReturn = _.template(volume)();
        break;
      case 'add' :
        toReturn = _.template(add)();
        break;
      default :
        toReturn = '';
        break;
    }
    return '<span class="sprite '+spriteCode+'">' + toReturn + '</span>';
  }); 

   //////////////////////////////////////////////////////////////////////////
  // I18N intern
  Handlebars.default.registerHelper('i18n', function( value){
      var _currentLocale = injector.get(injector.cfg.currentLocale);
      var _tradFromConfig = CfgClient.labels;

      if (_tradFromConfig[_currentLocale] && (_tradFromConfig[_currentLocale])[value])
        return (_tradFromConfig[_currentLocale])[value];

       if (_tradFromConfig[_tradFromConfig.default] && (_tradFromConfig[_tradFromConfig.default])[value])
        return (_tradFromConfig[_tradFromConfig.default])[value];
  });


  //////////////////////////////////////////////////////////////////////////
  // Pagination
   Handlebars.default.registerHelper('paginate', function( pagination,options ){

      if (!pagination)
        return '';

      var result='<nav>\n<ul class="pagination">';
      var maxNumPage=0;
        var numPageActive = 0;
        if (pagination) {
          _.each(pagination,function(_pagination) {
            result = result+'<li><a class="paginate-link '
            +(_pagination.active ? ' ' : 'disabled')+(_pagination.selected ? 'active' : '')
            +'" data-value="'+(_pagination.value-1)+'" '
            +'  >'+_pagination.value+'</a></li>';
            if (_pagination.selected)
              numPageActive = _pagination.value;
            if (_pagination.value>maxNumPage)
              maxNumPage=_pagination.value;
          });
        }

        result = '<label>Page '+numPageActive+'/'+maxNumPage+'</label>\n'+result;

        return result;
        /*
        var result='<nav>\n<ul class="pagination">';
        if (pagination) {
          _.each(pagination,function(_pagination) {
            result = result+'<li><a class="'+(_pagination.active ? ' ' : 'disabled')+(_pagination.selected ? 'active' : '')
            +'" '
            +(_pagination.selected || (! _pagination.active) ? '' : ' href="'+_pagination.url+'" ')+'  >'+_pagination.value+'</a></li>';
          });
        }

        return result;*/
    });

  

  //////////////////////////////////////////////////////////////////////////
  // Date
  Handlebars.default.registerHelper('selectdate', function( className, selectedDate,options ){
        var result='<div class="select-date-container selectdate_'+className+'">\n'
        //result=result+'<label>Mois</label>\n';
        result=result+'<select name="month">\n';
        var monthsNames = ['Janvier','Février','Mars','Avril','Mau','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'];
        for (var i=0;i<monthsNames.length;i++) {
          result=result+'<option value="'+(i+1)+'">'+monthsNames[i]+'</option>';
        }
        result=result+'</select>\n';

        //result=result+'<label>Année</label>\n';
        result=result+'<select name="year">\n';
         for (var i=1940;i<2016;i++) {
          if (selectedDate && selectedDate===i)
            result=result+'<option selected value="'+(i)+'">'+i+'</option>';
          else  
            result=result+'<option value="'+(i)+'">'+i+'</option>';
        }
        result=result+'</select>\n';
        result=result+'</div>';
        return result;
    });  


  //////////////////////////////////////////////////////////////////////////
  // Tools

  Handlebars.default.registerHelper('select', function( value, options ){
        var $el = $('<select />').html( options.fn(this) );
        $el.find('[value=' + value + ']').attr({'selected':'selected'});
        return $el.html();
    });

  Handlebars.default.registerHelper('t', function (key) {
    return key;// i18n[key] || key;
  });

  Handlebars.default.registerHelper('ifEqual', function (value1,value2,options) {
    if (value1===value2)
      return options.fn(this);
    return options.inverse(this);

  });

  Handlebars.default.registerHelper('valGenericList', function (value) {
    if (! value)
      return "";

    if (value.type && value.type==='html' && value.value)
      return value.value;//value.value;

    if (value)
      value = (""+value).replace(/</g,'');
    return value || '';
  });

  Handlebars.default.registerHelper('val', function (value) {
   
    if (value)
      value = (""+value).replace(/</g,'');
    return value || '';
  });

  Handlebars.default.registerHelper('valModel', function (value) {
    if (this.attributes && this.get(value)!==undefined && this.get(value)!==null) {
      var result= this.get(value)+"";
      if (result) 
        result=result.replace(/</g,'');
      return result;
    }
    return '';
  });

  //used for client side on Backbone object
  Handlebars.default.registerHelper('valTranslated', function (value) {
    if (this.attributes && this.getLabelI18N) {
      var result= this.getLabelI18N(value)+"";
      if (result) 
        result=result.replace(/</g,'');
      return result;
    }
    return '';
  });

  //used admin side 
  Handlebars.default.registerHelper('adminTranslated', function (obj,attrib,codeLocale) {
    if (! obj)
      return '';

    if (obj.attributes && obj.get(attrib)) {
      var objTranslations = obj.get(attrib);
      if (objTranslations[codeLocale])
        return objTranslations[codeLocale];
    }
    else if (obj[attrib]) {
      var objTranslations = obj[attrib];
      if (objTranslations[codeLocale])
        return objTranslations[codeLocale];
    }

    return '';
  });


  Handlebars.default.registerHelper('length', function (array) {
    if (array && array.length)
      return array.length;
    return 0;
  });

   Handlebars.default.registerHelper('debug', function (obj) {
    console.log('debugging : '+obj);
    console.dir(obj);
    return 'DEBUG';
  });



  var countries;

  Handlebars.default.registerHelper('country', function (code) {
    if (!countries) {
      try {
        countries = injector.get('allcountries');
      }
      catch (e) {
        // nothing
      }
    }
    var country = _.findWhere(countries, {iso3: code});
    return country && country.name || code;
  });

  //////////////////////////////////////////////////////////////////////////
  // Images

  var formatRe = /@/g;
  var formatPattern = '_@x@';

  Handlebars.default.registerHelper('img_model', function (attrib) {
    

    var path = this.get(attrib);

    if (!path) {
      return;
    }

    if (path.indexOf('http://')===0)
      return path;    

    return config.remotes[config.env] + config.images.basepathes[config.env] + path;
  });

  Handlebars.default.registerHelper('img', function (path, format) {
    if (!path) {
      return;
    }

    var filename = path;

    if (path.indexOf('http://')===0)
      return path;

    if (format) {
      var dot = path.lastIndexOf('.');
      var filename = path.substr(0, dot);
      var ext = path.substr(dot);

      filename = filename + formatPattern.replace(formatRe, format) + ext
    }

    var miaou = miaou ? miaou+1 : 0;
    if (window && window.catmode) {

      return 'http://thecatapi.com/api/images/get?format=src&type=gif&lenez='+miaou;
    }

    //return config.remote + config.images.basepath + filename;
    return config.remotes[config.env] + config.images.basepathes[config.env] + filename;
  });

  Handlebars.default.registerHelper('img_simple', function (path) {
    if (!path) {
      return;
    }

    var filename = path;
    //return config.remote + config.images.basepath + filename;
    return config.remotesFiles[config.env] /*+ config.images.basepathes[config.env]*/ + filename;
  });



  return Handlebars;
});
