# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Maxime Le Coz <lecoz@irit.fr>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Maxime Le Coz <lecoz@irit.fr>

from timeside.core import implements, interfacedoc 
from timeside.analyzer.core import Analyzer
from timeside.analyzer import Waveform
from timeside.api import IAnalyzer
from numpy import spacing
from collections import deque

class ModelLongTerm(object):
    '''
    '''

    def __init__(self,ordre,echantillon):
        '''
        
        Constructor
        
        '''
        
        self.ordre                      = ordre
        self.ft                         = [0]*(ordre+2)
        self.ftm1                       = [0]*(ordre+2)
        self.variance_f                 = [1]*(ordre+2)
        self.variance_b                 = [1]*(ordre+2)
        self.et                         = [0]*(ordre+2)
        self.cor                        = [0]*(ordre+2)
        self.length                     = 1
        self.erreur_residuelle          = 0
        self.variance_erreur_residuelle = 0

        oubli = 1.0/float(self.length) 

        self.variance_f[0] = self.variance_f[0]+oubli*(echantillon**2-self.variance_f[0])
        self.variance_b[0] = self.variance_f[0]   
        self.et[0]  = echantillon
        self.ft[0]  = echantillon
        
        ik = min([ordre,self.length-1])
        self.erreur_residuelle = self.et[ik]
        self.variance_erreur_residuelle =self.variance_f[ik]

    def miseAJour(self,echantillon):
        '''
        
        '''
                    
        self.length+=1
        self.ftm1 = self.ft[:]
        
        self.et[0] = echantillon      
         
        oubli = 1.0/float(self.length) 
        self.variance_f[0] = self.variance_f[0]+oubli*(echantillon**2-self.variance_f[0])
        self.variance_b[0] = self.variance_f[0]      
        ik = min([self.ordre,self.length-1])
        
        
        for n in xrange(ik+1) :
            oubli =1.0/float(self.length-n) 
            
            self.cor[n] = self.cor[n] + oubli*(self.ftm1[n]*self.et[n]-self.cor[n]) 
            
            knplus1 = 2*self.cor[n]/(self.variance_f[n] + self.variance_b[n])
            
            self.et[n+1] = self.et[n]-knplus1*self.ftm1[n] 
            self.ft[n+1] = self.ftm1[n]-knplus1*self.et[n]
            
            self.variance_f[n+1] =  self.variance_f[n+1]+oubli*(self.et[n+1]**2-self.variance_f[n+1])
            self.variance_b[n+1] =  self.variance_b[n+1]+oubli*(self.ft[n+1]**2-self.variance_b[n+1])
        
        self.ft[0]  = echantillon
        self.erreur_residuelle = self.et[ik+1]
        self.variance_erreur_residuelle =self.variance_f[ik+1] 

    def __str__(self):
        '''
        
        '''
        
        s  = 'Model Long Terme\n'
        s += '\tOrdre\t\t%d\n'%self.ordre
        s += '\tLongueur\t%d\n'%self.length
        s += '\tet\t\t['
        for e in self.et :
            s += '%f '%e
        s += ']\n'
        s += '\tft\t\t['
        for e in self.ft :
            s += '%f '%e
        s += ']\n'
        s += '\tft-1\t\t['
        for e in self.ftm1 :
            s += '%f '%e
        s += ']\n'
        s += '\tVarb\t\t['
        for e in self.variance_b :
            s += '%f '%e
        s += ']\n'
        s += '\tVarf\t\t['
        for e in self.variance_f :
            s += '%f '%e
        s += ']\n'       
        s += '\tErreur\t\t%f\n'%self.erreur_residuelle
        s += '\tVar(err)\t%f\n'%self.variance_erreur_residuelle  
        return s


        
class ModelCourtTrerm(object):
    '''
    '''
    
    def __init__(self,ordre,buff):
        '''
        
        Constructor
        
        '''
        
        self.N = len(buff)
        self.ordre = ordre
        self.erreur_residuelle = 0
        self.variance_erreur_residuelle = 0
        self.coef_autocorr = [0]*(self.ordre+2)
        self.AI = [0]*(self.ordre+2)
        self.dernier_echantillon = 0
        self.buff = buff
        for tau in xrange(self.ordre+1) :
            for i in xrange(self.N-tau):
                self.coef_autocorr[tau] =  self.coef_autocorr[tau]+buff[i]*buff[i+tau-1]
        self.estimModel()
        
    def estimModel(self):

        coef_reflexion = [0]*self.ordre
        
        if self.coef_autocorr[0] <= 0 :
            self.coef_autocorr[0] = 1.0
        
        coef_reflexion[0] = -self.coef_autocorr[1]/self.coef_autocorr[0]
        self.AI[0] = 1
        self.AI[1] = coef_reflexion[0]
        self.variance_erreur_residuelle = self.coef_autocorr[0]+self.coef_autocorr[1]*coef_reflexion[0] 
        
        if self.ordre > 1 :
            i_ordre = 1
            while i_ordre<self.ordre and self.variance_erreur_residuelle > 0  :

                if self.variance_erreur_residuelle > 0 :                    
                    S = 0
                    for i in xrange(i_ordre) :
                        S = S+self.AI[i]*self.coef_autocorr[i_ordre-i+1]
                        
                    # coef reflexion
                    coef_reflexion[i_ordre] = -S/self.variance_erreur_residuelle
                    
                    MH = i_ordre/2+1
                    for i in xrange(1,MH) :
                        
                        IB = i_ordre-i+2
                        tmp = self.AI[i]+coef_reflexion[i_ordre]*self.AI[IB]
                        self.AI[IB] = self.AI[IB]+coef_reflexion[i_ordre]*self.AI[i]
                        self.AI[i] = tmp 
                    self.AI[i_ordre+1] = coef_reflexion[i_ordre]
                    self.variance_erreur_residuelle = self.variance_erreur_residuelle+coef_reflexion[i_ordre]*S

                i_ordre+=1
                
        if self.variance_erreur_residuelle > 0 :
            self.variance_erreur_residuelle = self.variance_erreur_residuelle/float(self.N-1)
            self.erreur_residuelle = 0 
            for i in range(self.ordre+1) :
                self.erreur_residuelle = self.erreur_residuelle +self.AI[i]*self.buff[self.N-i-1]        
                
    def miseAJour(self,echantillon):
        self.dernier_echantillon = self.buff.popleft()
        self.buff.append(echantillon)
        for tau in xrange(1,self.ordre+1):
            self.coef_autocorr[tau] = self.coef_autocorr[tau]-self.dernier_echantillon*self.buff[tau-1]+self.buff[self.N-tau-1]*self.buff[self.N-1]
        self.coef_autocorr[0]       = self.coef_autocorr[0]  -self.dernier_echantillon**2+self.buff[self.N-1]**2
        self.estimModel()
        
    def __str__(self):
        '''
        '''
        s  = 'Model Court Terme\n'
        s += '\tOrdre\t%d\n'%self.ordre
        s += '\tAI\t['
        for e in self.AI :
            s += '%f '%e
        s += ']\n' 
        s += '\tErreur\t%d\n'%self.erreur_residuelle
        s += '\tVar(err)\t%d\n'%self.variance_erreur_residuelle
        s += '\tAutocor\t ['
        for e in self.coef_autocorr :
            s += '%f '%e
        s += ']\n'        
        return s     


def calculDistance(modeleLong,modeleCourt):
    '''
    Calcul de la distance entre les modèles longs et court terme
    
    args :
        - modeleLong (ModelLongTerme) : Modèle appris sur tous les echantillons depuis la dernière rupture
        - modeleCourt (ModelCourtTrerm): Modèle appris sur les Lmin derniers echantillons 
    '''
    
    if modeleCourt.variance_erreur_residuelle == 0 :
        # epsilon pour le type de donnés correspondant à modeleLong.variance_erreur_residuelle
        numerateur = spacing(modeleCourt.variance_erreur_residuelle)
    else :
        numerateur = modeleCourt.variance_erreur_residuelle
            
    QV= numerateur/modeleLong.variance_erreur_residuelle
    return (2*modeleCourt.erreur_residuelle*modeleLong.erreur_residuelle/modeleLong.variance_erreur_residuelle-(1.0+QV)*modeleLong.erreur_residuelle**2/modeleLong.variance_erreur_residuelle+QV-1.0)/(2.0*QV)


def segment(data,fe,ordre=2,Lmin=0.02,lamb=40.0,biais=-0.2,with_backward=True,seuil_vois=None,withTrace = False):
    '''
    Fonction principale de segmentation.
    
    args : 
        - data (list of float): echantillons du signal
        - fe  (float) : fréquence d'échantillonage
        - ordre (int) : ordre des modèles. Par défaut = 2
        - Lmin (float) : longeur minimale d'un segment et taille du buffer pour l'apprentissage du model court terme. Par défaut = 0.02
        - lamb (float) : valeur de lambda pour la détection de chute de Wn. Par défaut = 40.0
        - biais (float) : valeur du bias à appliquer (en négatif). Par défaut = -0.2
        - with_backward (Bool) : Interrupteur du calcul ou non en backward. Par défaut = True
        - seuil_vois (float) : Si fixé, défini les valeurs de lambda et du biais en fonction du voisement ou non du buffer initial du model court terme.
                               (voisement_yin >  seuil_vois ==> Non voisé). Par défaut = None
        - withTrace (Bool) : Enregistre ou non la trace de tous les calculs pour un affichage à postériori. Par défaut = False 
    
    '''
    # Initialisation
    frontieres = []    
    t = 0 
    rupt_last = t 
    long_signal = len(data)
    # taille minimum en echantillons
    Lmin = int(Lmin*fe)

    while t < long_signal-1 :
        # Nouvelle Rupture
        
        #    Critere d'arret : decouverte d'une rupture
        rupture = False
        
        # Cumulateur de vraissemblance
        Wn = 0.
        
        # Valeur et emplacement de la valeur max
        maxi = (0,-1)
        
        audio_buffer = deque([],Lmin)
            
        # Initialisation du modèle long terme
        echantillon= data[t]
        longTerme = ModelLongTerm(ordre,echantillon)
            
        while (not rupture) and t < long_signal-1  : 
            
            t+=1
            
            # Mise à jour du long terme
            echantillon = data[t]
            longTerme.miseAJour(echantillon)

            # Si l'ecart avec la dernière rupture est suffisant
            # pour utiliser le modèle court terme 
            if t-rupt_last >= Lmin :
                
                # Initialisation du modèle court terme
                if t-rupt_last == Lmin :
                    courtTerme = ModelCourtTrerm(ordre, audio_buffer)
                    
                # Mise à jour du modèle court terme                               
                if t-rupt_last > Lmin :
                    courtTerme.miseAJour(echantillon)
                
                # mise à jour du critère
                Wn = Wn+calculDistance(longTerme,courtTerme)-biais
                
                # Recherche de nouveau maximum
                if Wn > maxi[0] :
                    maxi = (Wn,t)
                
                if withTrace :
                    dynaWn += [Wn]
                    tWn += [t]
                    
                # Recherche de rupture par chute superieure à lambda
                if (maxi[0] - Wn) > lamb :
                    rupture = True
            else :
                # Sinon, on prepare l'initialisation
                audio_buffer.append(echantillon)
        
        # Positionnement de la rupture au dernier point maximum        
        t_rupt = maxi[1]
        
                
        # Si une rupture à été detecté avec un modèle stable (Wn à croit)   
        if t_rupt > -1 :
            
            m = 'forward'                
            if with_backward :
                
                bdata = data[t_rupt:rupt_last:-1]
                
                if len(bdata) > 0 :
                
                    front = segment(bdata,fe,ordre,float(Lmin)/fe,lamb,biais,with_backward=False,seuil_vois=seuil_vois,withTrace=withTrace)
                    t_bs = [ t_rupt-tr for tr,_ in front]
                    
                    if len(t_bs) > 0 :
                        t_rupt = t_bs[-1]
                        m ='backward'
                    
        # Sinon on crée un segment de longueur minimale
        else :
            t_rupt = rupt_last+Lmin
            m = 'instable'
            
        if withTrace :
            evnt['selected'] = t_rupt
            evnt['comment'] = m
            trace+=[evnt]

        # Mise à jour des frontières
        t = t_rupt 
        rupt_last = t_rupt
        
        if rupture :
            frontieres.append((t_rupt,m))
            
    return frontieres



class IRITDiverg(Analyzer):
    implements(IAnalyzer)
    '''
    '''
    def __init__(self, blocksize=1024, stepsize=None) :
        super(IRITDiverg, self).__init__();
        self.parents.append(Waveform())
        self.ordre = 2


    @interfacedoc
    def setup(self, channels=None, samplerate=None,blocksize=None, totalframes=None):
        super(IRITDiverg, self).setup(channels,
                                      samplerate,
                                      blocksize,
                                      totalframes)
        self.parents.append(Waveform())
    @staticmethod
    @interfacedoc
    def id():
        return "irit_diverg"

    @staticmethod
    @interfacedoc
    def name():
        return "IRIT Forward/Backward Divergence Segmentation"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Stationnary Segments"

    def process(self, frames, eod=False):
        '''

        '''
        return frames, eod

    def post_process(self):
        data = self.process_pipe.results['waveform_analyzer'].data       
        frontieres = segment(data,self.samplerate(),self.ordre)
        f = open('front.lab','w')
        for t,m in frontieres :
            f.write('%f\t%s\n'%(float(t)/self.samplerate(),m));
        f.close()
        print frontieres
