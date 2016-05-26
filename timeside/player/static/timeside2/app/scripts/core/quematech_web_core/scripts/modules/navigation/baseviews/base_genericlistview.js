define([
  './base_qeopaview',
  '#qt_core/controllers/all',
  './subs/sub_array_genericlist'
],


/**
  This is a generic list item. paramaters are : 
    {
      title
      hasAllData : nous dit si la liste a toutes les datas (notamment si champs de recherche) ou doit faire des appels serveur
      showFilter : montre un champs de filtrage


      onRender : called with this = view
      onDestroy : called with this = view

      eventForFilter : event envoyé pour mettre à jour la data (on mettra avant à jour injector.get('searchTerm'))
      eventDelete : event envoyé pour supprimer l'élément
      viewId : utilisé pour rafraichir la liste (en lançant un évènement de nav), genre après un delete
      url : main url for pagination (like /#type_data/list)
      newButton : {
        label
        url
      }
      injectorListId : id for finding data in injector
      beforeShowDataFunc : _func on direct data BEFORE transforming into JSON. here manage getters if not directly
      list : {
        //// ORDER MATTERS!
        headers : [] can be string (function?)
        getters : [] getter to use to show parameter value in tab. MUST be string : we look at the parameter of the JSON object
      }
    }
**/
function (BaseQeopaView,A,ArrayView) {
  'use strict';

  return BaseQeopaView.extend({


    ////////////////////////////////////////////////////////////////////////////////////
    //View definition

    template: templates['navigation/base_genericlist'],
    className: 'generic_list',

    initialize: function (options) { 
        if (! options.listParameters)
          throw new Error('calling generic list without parameters');
        if (options.listParameters.isMultiple) {
          var _type = A.injector.get(A.injector.cfg.currentTypeData);
          this.listParameters = options.listParameters[_type];
          if (! this.listParameters)
            console.error('No list parameters on multiple for '+_type);
        }
        else {
          this.listParameters = options.listParameters;
        }

        this.allData = A.injector.get(this.listParameters.injectorListId);
        this.filteredData = this.allData;

        this.inputFilterText = "";

        
    },


    onRender:function() {
      if (this.arrayCreated) {
        this.arrayView.destroy();
        this.arrayCreated=false;
      }

      if (! this.arrayCreated) {
        this.arrayView = new ArrayView();
        this.arrayCreated=true;
        this.arrayView.setData(this.listParameters.list.headers,this.prepareDataForArray());
        this.arrayView.setDaddy(this);
        this.ui.containerArray.empty().append(this.arrayView.render().$el);
      }

      if (this.listParameters && this.listParameters.onRender && _.isFunction(this.listParameters.onRender))
        this.listParameters.onRender(this);

    },


    onDestroy: function () {
      if (this.listParameters && this.listParameters.onDestroy && _.isFunction(this.listParameters.onDestroy))
        this.listParameters.onDestroy(this);
    },

    ui : {
      containerArray : '.generic_array_container',
      inputFilter : '.generic_list_filter',
      linkPaginate : '.paginate-link'
    },

    events : {
      'input @ui.inputFilter' : 'onFilterChangeSwitch',
      'click @ui.linkPaginate' : 'onClickPaginate'
    },

     ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    //Pagination management.
    onClickPaginate:function(evt) {
      var numPage = parseInt(evt.currentTarget.dataset.value);
      if (! _.isFinite(numPage))
        return console.error('Numpage error '+numPage);

      this.currentPagination = numPage;
      this.refreshContentFromServer();
    },

    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    //Filter management. On ne descend qu'à deux niveaux en données locales

    onFilterChangeSwitch:function(ev) {
      if (! this.trueSearchFunction)
        this.trueSearchFunction = _.debounce(_.bind(this.actualFilterChangeSwitch,this),300);

      return this.trueSearchFunction(ev); //_.debounce
      /*if (this.listParameters.hasAllData)
        return this.onFilterChange(ev);
      else
        return this.onServerFilterChange(ev);*/
    },

    actualFilterChangeSwitch:function(ev) {
      if (this.listParameters.hasAllData)
        return this.onFilterChange(ev);
      else
        return this.onServerFilterChange(ev);
    },

    /////////////////////////
    //filter change when server call needed
    onServerFilterChange:function(ev) {
      var txtIn = this.ui.inputFilter.val();
      this.inputFilterText = txtIn;
      if (! this.listParameters.eventForFilter)
        return console.error('No event for filter!');

      A.injector.set(A.injector.cfg.currentSearchTerm, txtIn);
      this.currentSearchTerm = txtIn;
      this.currentPagination=0;
      this.refreshContentFromServer();
     
    },


    //Called by pagination && serverFilterChange
    refreshContentFromServer:function() {
      var self=this;
      var dataServer = {term : this.currentSearchTerm, page : this.currentPagination}
      A.ApiEventsHelper.listenOkErrorAndTrigger2(
        this.listParameters.eventForFilter,dataServer,null,function(result) {
          A.injector.set(A.injector.cfg.currentListData,result);
          self.onServerFilterResult(result);
      },function(error) {
          console.error('Update config list error ');
      },this);

    },

    onServerFilterResult:function(result) {
      this.filteredData = result;
      this.arrayView.setData(this.listParameters.list.headers,this.prepareDataForArray());
      this.render();
    },

    /////////////////////////
    //filter change when all data in array
    onFilterChange:function(ev) {
      var txtIn = this.ui.inputFilter.val();
      this.inputFilterText = txtIn;
      if ((! txtIn) || txtIn.length===0) {
        this.filteredData = this.allData;
        this.arrayView.setData(this.listParameters.list.headers,this.prepareDataForArray())
        return;
      }

      var functionFilter = function(obj) {
        var testObj = obj.attributes ? obj.attributes : obj;
        console.log('\ntesting object : '+JSON.stringify(testObj));

        var objIsInFilter = _.find(testObj,function(value,attrib) {
          console.log('     testing on '+value);
          if (_.isString(value))
            return value.indexOf(txtIn)>=0;
          else if (_.isNumber(value))
            return (value+"").indexOf(txtIn)>=0;
          else          
            return functionFilter(value);

        });
        console.log('!!!!Result : '+JSON.stringify(objIsInFilter));
        return objIsInFilter!==undefined;
      };


      var filteredData = _.isArray(this.allData) ? _.filter(this.allData,functionFilter) 
        : (this.allData.models ? this.allData.filter(functionFilter) : []);
      this.filteredData = filteredData;

      this.arrayView.setData(this.listParameters.list.headers,this.prepareDataForArray())
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Managing delete
    deleteItem:function(id) {
      var eventDelete = this.listParameters.eventDelete;
      if (! eventDelete)
        return console.error('no Event delete defined');

      this.currentDeleteId = id;
      A.vent.trigger(A.Cfg.events.ui.notification.show, 
          {type : 'warning', title : 'Deleting',text : 'Are you sure you want to delete this item?',
          actions : [
            {label : 'Delete', type : 'danger', callback : _.bind(this.onDeleteOk,this)},
            {label : 'Cancel', type : 'info', callback :  _.bind(this.onDeleteCancel,this)}
          ]});

      var eventArg = _.clone(this.listParameters.eventDeleteArg);
      if (! eventArg)
        eventArg = {};
      eventArg['id'] = id;

     

    },

    onDeleteCancel:function() {
      A.vent.trigger(A.Cfg.events.ui.notification.hide);
    },

    onDeleteOk:function() {
      var eventDelete = this.listParameters.eventDelete;
      var eventArg = _.clone(this.listParameters.eventDeleteArg);
      if (! eventArg)
        eventArg = {};
      eventArg['id'] = this.currentDeleteId;

      var self=this;
      A.ApiEventsHelper.listenOkErrorAndTrigger2(
        eventDelete,eventArg,null,function(result) {
          if (self.listParameters.viewId)
            A.vent.trigger('navigate:page',self.listParameters.viewId);
          else
            window.location.reload(); //worst case scenario
        },function(error) {
          console.log('genericlist - unknown error delete');
        },this);

      A.vent.trigger(A.Cfg.events.ui.notification.hide);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Preping data for array
    prepareDataForArray :function() {
      var _dataOk = [];
      var _dataIn = this.filteredData;//A.injector.get(this.listParameters.injectorListId);


      if (_.isFunction(this.listParameters.beforeShowDataFunc))
        _dataIn = this.listParameters.beforeShowDataFunc(_dataIn); //scope?

      //getting array of JSON objects
      if (_dataIn.models) { //quickie to know if this is a collection
        _dataOk = _dataIn.map(function(_objIn) {return _objIn.toJSON ? _objIn.toJSON() : _objIn});
      }
      else if (_.isArray(_dataIn)) {
        _dataOk = _.map(_dataIn,function(_objIn) {
          return _objIn.toJSON ? _objIn.toJSON() : _objIn
        });
      }


      //generating data for array. Keeping (praying) for getters order.
      _.each(_dataOk,function(_data) {
        _data.computed_values = [];
        _.each(this.listParameters.list.getters,function(_getter) {
          //must be String or Function. @TODO checking type. 
          var _value = _.isString(_getter) ? _data[_getter] : _getter(_data);

          _data.computed_values.push(_value);
        },this); 
      },this);

      return _dataOk;
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Managing data
    serializeData: function () {
      
      var _paginateData = A.injector.get(A.injector.cfg.pagination_data);
      var _pagination = _paginateData ? this.generatePaginationData(this.listParameters.url,0,_paginateData.totalPages-1,_paginateData.number)
        : undefined;


      //var _pagination = this.generatePaginationData(this.listParameters.url,1,100,48);
      return {
        mainTitle : this.listParameters.title,
        newBtnConfig : this.listParameters.newButton,
        /*items : _dataOk,*///injector.get(injector.cfg.currentListData) ? injector.get(injector.cfg.currentListData).toJSON() : [],
        paginate : _pagination,
        /*headers : this.listParameters.list.headers,*/
        showFilter : this.listParameters.showFilter,
        inputFilterText : this.inputFilterText
        /*,
        getters : this.listParameters.list.getters*/
      }
    },

    
   
  });
});
