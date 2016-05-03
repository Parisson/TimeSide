define([
  'backbone.associations',
  '../../qeopa_basemodel',
  './menu_regleselection'
],

function (Backbone,QeopaBaseModel,RegleSelectionModel) {

  'use strict';

  /**
  Warning : 
    Un menu contient des règlesSelections qui regroupent des sélections par règles
    Un objectif est donc de créer le orderedSelection
  **/
  return QeopaBaseModel.extend({
    defaults: {
      intern_type : 'menu',
      id : 0,
      titre : {},
      prixBase : 0,
      axeJour : '',
      axeSemaine : '',
      selections : [], //regles
      visuel : null,

      //dynamic
      orderedSelections : [],

      disponibilitesDate : 0,
      disponibilitesHeure : 0,

      //dynamic while selecting a menu
      //warning : when item added to alreadyUsed, automatically added to alreadySeen...
      alreadyUsedSelection : [], //true array used in commande controller for following what we saw in a menu
      alreadySeenSelection : [] //idem but selection just seen, not chosen by user in menu
    },

    relations: [{
      type: Backbone.Many,
      key: 'selections',
      relatedModel: RegleSelectionModel
    },
    {
      type: Backbone.Many,
      key: 'orderedSelections',
      relatedModel: RegleSelectionModel
    },
    ],


    ////////////////////////////////////////////////////////////////////////////////////
    // methos for regles & choix commande
     initFromServer:function() {
      if (this.get('nom')) 
        this.set('titre',this.get('nom'));


      
      if (this.get('tarif')) {
        this.set('prixBase',this.get('tarif'));
      }
    },

    //called by commande.js
    resetUsedSelections:function() {
      this.set('alreadyUsedSelection',[]);
      this.set('alreadySeenSelection',[]);
    },

    //called by commande.js when selection chosen
    selectionHasBeenChosen:function(selection) {
      this.get('alreadyUsedSelection').push(selection);
      this.get('alreadySeenSelection').push(selection);
    },

    //called by commande.js whene selection seen but jumped
    selectionHasBeenSeen:function(selection) {
      this.get('alreadySeenSelection').push(selection);
    },


    findRegleWhereSelection:function(currentSelection) {
      var _regleSelectionForCurrentSelection = this.get('selections').find(function(_regleselection) {
        if (_regleselection.get('selections')) {
          var _selectionInRegle = _regleselection.get('selections').find(function(_testSelection) {
            return _testSelection.get('id')===currentSelection.get('id');
          });
          if (_selectionInRegle && _selectionInRegle.get('id')===currentSelection.get('id'))
            return true;
          return false;
        }
      });
      
      return _regleSelectionForCurrentSelection;
    },

    /*Depending of what we already selected, can we ? */
    canDisplaySelection:function(selection) {
      var _regle = this.findRegleWhereSelection(selection);
      if (_regle.get('typeRegle')==="ET")
        return true;

      if (_regle.get('typeRegle')==="OU") {
        //check if selection from this regle is already used
        var _regleAlreadyUsed = false;
        _.each(this.get('alreadyUsedSelection'),function(_usedSelection) {
          if (_regle.hasSelection(_usedSelection))
            _regleAlreadyUsed=true;
        });

        return !_regleAlreadyUsed;
      }
      return true;
    },

    /*Depending of what we already selected, can we ? */
    canJumpSelection:function(selection) {
      var _regle = this.findRegleWhereSelection(selection);
      if (_regle.get('typeRegle')==="ET")
        return false;

      if (_regle.get('typeRegle')==="OU") {
        //check if selection from this regle is already used
        var _regleAlreadyUsed = false;
        _.each(this.get('alreadyUsedSelection'),function(_usedSelection) {
          if (_regle.hasSelection(_usedSelection)) {
            _regleAlreadyUsed=true;
          }
        });

        //si déjà utilisée, ça n'a pas de sens mais bon...
        if (_regleAlreadyUsed)  
          return false;

        var _numFoisRegleSeen = 0;
         _.each(this.get('alreadySeenSelection'),function(_seenSelection) {
          if (_regle.hasSelection(_seenSelection)) {
            _numFoisRegleSeen++;
          }
        });

        //il faut que ce soit au pire l'avant dernier à être présenté pour être sauté.
        return ( !_regleAlreadyUsed && _numFoisRegleSeen<_regle.get('selections').length-1);
      }
    },    


    ////////////////////////////////////////////////////////////////////////////////////
    // getter
    getAllMeals:function() {
      var result = [];
      this.get('selections').each(function(_regleSelection) {
          //_regleSelection.genereTranslateFake(['_titre'],['titre']);
          _regleSelection.get('selections').each(function(_selection) {
              _selection.get('plats').each(function(_plat) {
                result.push(_plat);
              })
          });
      });
      return result;
    },


    ////////////////////////////////////////////////////////////////////////////////////
    // update attribs


    updateFakeTrads:function() {
      this.genereTranslateFake(['_titre'],['titre']);
      this.get('selections').each(function(_regleSelection) {
          //_regleSelection.genereTranslateFake(['_titre'],['titre']);
          _regleSelection.get('selections').each(function(_selection) {
              _selection.genereTranslateFake(['_titre'],['titre']);
              _selection.get('plats').each(function(_plat) {
                _plat.genereTranslateFake(['_titre'],['titre']);
              });
          });
      });

    },

    updateAttribs:function(){
        var allSelections = [];
      if (this.get('selections')) {
        this.get('selections').each(function(_regleSelect) {
          _regleSelect.updateAttribs();
          if (_regleSelect.get('selections'))
            allSelections = _.union(allSelections,_regleSelect.get('selections').models);
        })

        allSelections = _.sortBy(allSelections,function(_select) {
          return _select.get('orderInMenu');
        });
      }
       this.set('orderedSelections',new Backbone.Collection(allSelections));
    }
  });
});
