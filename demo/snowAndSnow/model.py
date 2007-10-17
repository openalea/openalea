#!/usr/bin/env python
"""model.py

Snow&Snow phyllotaxis model.

:version: 
:author:  szymon stoma
"""


from visual import *
import math
from matplotlib import rc, rcParams,use
rc('text', usetex=True )
use('Qt4Agg')
import pylab as pl
import random
import pickle
import sys
import  openalea.plotools.plotools as oa_plotools
import  openalea.plotools.plotable as oa_plotable
import openalea.plantgl.all as pgl
import openalea.plantgl.ext.all as pd
#import openalea.mersim.gui.phyllotaxis as phyllotaxis
import phyllotaxis

"""This code is due to pickling of the visual boost
python objects (vectors in this case).
"""
#import copy_reg
#def dump_visual_vector( v ):
#    return (vector, ( v.x,v.y,v.z ) )
#copy_reg.pickle(vector, dump_visual_vector)

red= pgl.Material( name="Mred",
              ambient=pgl.Color3(250,0,10),
              diffuse=1,
              specular=pgl.Color3(50,50,50),
              emission=pgl.Color3(0,0,0),
              shininess=1,
              transparency=0.4)
green= pgl.Material( ambient=pgl.Color3(0,250,10),
                 diffuse=1,
                 specular=pgl.Color3(50,50,50),
                 emission=pgl.Color3(0,0,0),
                 shininess=1,
                 transparency=0.4)
blue = pgl.Material( ambient=pgl.Color3(0,0,250),
                 diffuse=1,
                 specular=pgl.Color3(50,50,50),
                 emission=pgl.Color3(0,0,0),
                 shininess=1,
                 transparency=0.4)
black = pgl.Material( ambient=pgl.Color3(0,0,0),
                 diffuse=1,
                 specular=pgl.Color3(50,50,50),
                 emission=pgl.Color3(0,0,0),
                 shininess=1,
                 transparency=0.)


class ExceptionTooManyCandidates(Exception):
    """ To be thrown when more than one primordium can be created. In this situation the
    computations should be repeated with shorter step.
    """
    pass


class DiscInhibitorPhyllotaxisModel:
    """Class for simulating Snow&Snow phyllotaxis model.
    """
    def __init__( self, prims=None, visualisation=False ):
        self.c_center = vector(0,0,0)
        self.c_czone=1

        self.c_discretization =360
        self.c_plane_normal=vector(0,0,1)
        self.c_convergance_error = 1.
        self.c_convergance_nbr_last_values = 20
        
        self.c_prim_stiffness=14
        self.c_prim_trash=5
        self.c_prim_size=  4.1
        #: these values are used to determine the inhibition function 
        
        self.c_initial_timestep = 0.01
        self.c_timestep_treshold = 0.0001
        self.c_dzone  = 20*self.c_czone
        self.c_v0 = 1.
        self.c_show_inhibition_fields = True
        self.c_show_primordia = False
        

        self.c_visual_zone_size=0.01       
        
        # required for simulation
        self.current_timestep = self.c_initial_timestep
        self.time = 0
        self.current_prim = 0
        self.prims = {}
        self.i_prim2time = {}
        self.i_prim2init_pos = {}
        
        self._check_convergance = 0
        
        self.init_prims(prims)
        
        if visualisation: self.visualisation = 1
        else: self.visualisation=0
            # cropping we -- do not care for visual anymore.
            # 0 none, 1 plantgl, 2 visual
        if self.visualisation>0:
            self.prepare_scene()
            self.vis = []
   
    def converges( self, error=None ):
        """Returns True iff we observe converging to ONE angle value with given error.
        """
        y = []
        z = len(self.i_prim2init_pos)
        for j in range( z-10,z):
            y.append( phyllotaxis.standarize_angle( phyllotaxis.get_angle_between_primordias( self.i_prim2init_pos[ j], self.i_prim2init_pos[ j-1]) ) )
        for i in range( 2,len(y) ):
            if abs( y[ -1 ] - y[ i ] )  > error:
                return False
        return True        

    def check_convergance( self, how_many_last_values=None ):
        """Use to check if system converges. Returns True if it converges. 
        """
        if self._check_convergance < self.current_prim:
            self._check_convergance = self.current_prim
            if self.current_prim > how_many_last_values:     
                return self.converges(error=self.c_convergance_error)
            else:
                return False
        
    def f_single_inihibition( self, p1, p2, r):
        """Defines the behaviour of single primordium inhibition.
        """
        d = mag(p1 - p2)
        try:
            return (self.c_prim_size/d)**self.c_prim_stiffness
        except ZeroDivisionError:
            return float(1000000000)

    def f_inhibition( self, v, prims ):
        """Defines the Inhibition function.
        """
        r = 0
        for i in prims:
            r += self.f_single_inihibition( v, prims[ i ], self.c_prim_size)
        return r
    
    def displacement( self, p, c ):
        """Defines how the primordias are moving.
        """
        return norm( p-c )*self.scalar_speed( p )

    def scalar_speed( self, p ):
        """Defines the magnitude with which primordias are moving.
        """
        return self.current_timestep*self.c_v0*mag(p-self.c_center)/self.c_czone

    def prepare_scene( self ):
        """Visualisation. It is not mandatory.
        """
        if self.visualisation==1:
            self.scene = pgl.Scene()
            self._prepare_scene()
            pgl.Viewer.camera.lookAt( pgl.Vector3( 0,0,20 ), pgl.Vector3( 0,0,0 ) )
            pgl.Viewer.camera.setOrthographic()
            pgl.Viewer.animation( True )
            pgl.Viewer.display( self.scene )
        else:
            self.background = cylinder(pos=vector(0,0,-1), axis=vector(0,0,1),radius=1.5*self.c_dzone, length=0.01, color=(0.,0.0,0))
            self.center = sphere(pos=vector(0,0,1), radius=0.1, color=(1,1,1))
            self.competence = ring( pos=vector(0,0,1), axis=vector(0,0,1), radius=self.c_czone, thickness=self.c_visual_zone_size)
            self.drop = ring( pos=vector(0,0,1), axis=vector(0,0,1), radius=self.c_dzone, color=(1,0,0), thickness=self.c_visual_zone_size)
            scene.exit_on_close( 0 )

    def _prepare_scene( self ):
        """Visualisation. It is not mandatory.
        """
        self.drop = pgl.Shape( pgl.Disc(self.c_dzone), black )
        self.center = pgl.Shape( pgl.Translated( pgl.Vector3(0,0,0.1 ), pgl.Sphere( radius=0.1 ) ), red )
        self.competance_zone = pgl.Shape( pgl.Translated( pgl.Vector3(0,0,0.1), pgl.Disc( self.c_czone) ), blue )
        self.scene.add( self.competance_zone )
        self.scene.add( self.center )
        self.scene.add( self.drop )
            

    def visualise_prims( self, prims, vis ):
        """Visualisation. NOT mandatory.
        """
        if self.visualisation == 2:        
            nv=[]
            for i in vis:
                i.visible=False
            for i in prims:
                nv.append( cylinder(pos=prims[ i ], axis=vector(0,0,1),radius=self.c_prim_size, length=0.01*(self.c_dzone-mag(self.c_center-prims[ i ])), color=(0.,0.5,0)))
                nv.append( ring(pos=prims[ i ], axis=vector(0,0,1),radius=self.c_prim_size, thickness=0.008*(self.c_dzone-mag(self.c_center-prims[ i ])), color=(0.,0.8,0)))
                nv.append( cylinder(pos=prims[ i ], axis=vector(0,0,1),radius=float(self.c_prim_size)/25, length=50, color=(0.5,0.0,0)))
            #raw_input()    
            return nv
        else:
            nv = []
            # start walkaround
            self.scene.clear()
            self._prepare_scene()
            #end walkaround
            
            for i in prims:
                if self.c_show_inhibition_fields:
                    p = pgl.Shape(
                            pgl.Translated(
                                pgl.Vector3( prims[ i ].x, prims[ i ].y, prims[ i ].z+0.2 ),
                                pgl.Disc( self.c_prim_size )
                            )
                            , red )
                    nv.append( p )
                    self.scene.add( p )
                if self.c_show_primordia:
                    p = pgl.Shape(
                            pgl.Translated(
                                pgl.Vector3( prims[ i ].x, prims[ i ].y, prims[ i ].z+0.2 ),
                                pgl.Disc( self.c_prim_size/100 )
                            )
                            , red )
                    nv.append( p )
                    self.scene.add( p )
            pgl.Viewer.update()
            return nv

    def competance_grid( self ):
        """Returns a list of points where new primordia could be formed.
        """
        l = []
        e = random.random()
        for i in range(self.c_discretization):
            a = e+(float(i)/self.c_discretization)*2*math.pi
            x = self.c_czone*math.cos(a)
            y = self.c_czone*math.sin(a)
            l.append(vector(x,y,0))
        #second ring
        for i in range(self.c_discretization/4):
            a = e+(float(i)/self.c_discretization/5)*2*math.pi
            x = 1.1*self.c_czone*math.cos(a)
            y = 1.1*self.c_czone*math.sin(a)
            l.append(vector(x,y,0))
        return l

    def move_primodiums( self, prims ):
        """Moves all primordia acording to displacement.
        """
        for i in prims:
            prims[ i ] = prims[ i ] + self.displacement(prims[ i ], self.c_center)
        return prims

    def drop_primordiums( self, prims ):
        """Removes primordia from simulation.
        """
        t = {}
        for i in prims:
            if mag(prims[ i ] - self.c_center) < self.c_dzone:
                t[ i ] = prims[ i  ]
        return t

    def search_new_primordiums( self, prims, cand ):
        """Checks if new primordia can be added (based on the inhibition field intensity).
        """
        appcand=[]
        for i in cand:
            if  self.f_inhibition(i, prims) <= self.c_prim_trash:
                appcand.append( i )
        return appcand

    def insert_new_primordiums( self, prims ):
        """Inserts new primordium in the cycle of primordium update.
        """
        cand = self.competance_grid()
        appcand = self.search_new_primordiums( prims, cand)
        if len( appcand ) > 1:

            if self.current_timestep > self.c_timestep_treshold:
                raise ExceptionTooManyCandidates()
            else:
                pass
                #print " !: sorting.."
        self.prims = prims.copy()
        while len(appcand):
            appcand = self.sort_prim_cand( prims=self.prims, prim_cand=appcand) 
            self.add_prim( appcand[ 0 ] )
            appcand = self.search_new_primordiums( prims=self.prims, cand=appcand)

    def sort_prim_cand( self, prims=None, prim_cand=None):
        """Sorts primordia according toinhibition function
        """
        if len( prim_cand ) < 2:
            return prim_cand
        ds = {}        
        for i in prim_cand:
            ds[ i ] = self.f_inhibition( i, prims )
        prim_cand.sort( lambda x, y: cmp( ds[ y ],  ds[ x ] ))
        return prim_cand    


    def add_prim( self, prim ):
        """Inserts new primordium, updating all information about primordium creation.
        """
        self.prims[ self.current_prim ] = prim
        self.i_prim2init_pos[ self.current_prim ] = prim
        self.i_prim2time[ self.current_prim ] = self.time
        self.current_prim += 1
        print self.current_prim
    

    #def get_angle_between_primordias( self, i, j):
    #    """ Returns angle between primordias. Angle is in degrees [0,360) and is always
    #    calculated with the same chirality.
    #    """
    #    p = self.i_prim2init_pos
    #    yi = p[ i ]
    #    yj = p[ j ]
    #    yi.z = 0
    #    yj.z = 0
    #    d = yi.diff_angle(yj)
    #    if mag( rotate( yi, axis=self.c_plane_normal, angle=d )- yj ) < 0.001:
    #        return d*360/(2*math.pi)
    #    else:
    #        return (2*math.pi-d)*360/(2*math.pi)
    #
        
    def run( self, nbr_prim=sys.maxint ):
        """Main loop.
        """
        while not len( self.i_prim2init_pos ) > nbr_prim:
            primordiumsT = self.prims.copy()
            primordiumsT = self.move_primodiums( primordiumsT )
            try:
                self.time += self.current_timestep
                self.insert_new_primordiums( primordiumsT )
            except ExceptionTooManyCandidates:
                self.time -= self.current_timestep
                self.current_timestep = self.current_timestep/10
                #print " #: decreasing dt.."
                continue
            self.current_timestep = self.c_initial_timestep
            if self.visualisation>0:
                self.vis = self.visualise_prims( prims=self.prims, vis=self.vis )            
            self.prims = self.drop_primordiums(self.prims)
            if self.check_convergance(how_many_last_values=self.c_convergance_nbr_last_values):
                break
            
    def init_prims( self, prims=None ):
        """Inits primordias.
        """
        if not prims == None:
            for i in prims:
                self.add_prim( prims[ i ] )
        else:
            self.add_prim( vector(-self.c_czone,0,0) )
            self.add_prim( vector(self.c_czone+0.01,0,0) )



def plot_time_diff( timeD, min_gamma=None, max_gamma=None, how_many_last_values=10 ):
    """Plots time difference between succeding primordias for many gammas.
    """
    y = []
    x = []
    for i in timeD:
        if i <= max_gamma and i >= min_gamma:
            k = len( timeD[ i ] )
            for j in range(k-how_many_last_values, k):
                x.append( i )
                y.append( timeD[ i ][ j] - timeD[ i ][ j-1])
    pl.plot( x, y, "." )
    pl.show()    

def plot_divergance_angle( divD, min_gamma=None, max_gamma=None, how_many_last_values=10 ):       
    """Plots divergance angels between succeding primordias for many gammas.
    """
    y = []
    x = []
    for i in divD:
        if i <= max_gamma and i >= min_gamma:
            k = len( divD[ i ] )
            for j in range(k-how_many_last_values, k):
                x.append( i )
                y.append( phyllotaxis.standarize_angle( phyllotaxis.get_angle_between_primordias( divD[ i ][ j], divD[ i ][ j-1]) ) )
    pl.plot( x, y, "." )
    pl.show()    
    


def plot_divergance_angle_change( divD, gamma ):       
    y = []
    x = []
    i = gamma
    plot_divergance_angle_change_for_single_gamma( divD[ i ] )



def generate_plotable_data_divergance_angle_change_for_single_gamma( divD ):       
    y = []
    x = []
    for j in range( 1,len( divD ) ):
        x.append( j )
        y.append( phyllotaxis.standarize_angle( phyllotaxis.get_angle_between_primordias( divD[ j], divD[ j-1]) ) )
    return oa_plotable.plotObject( x=x, y=y, legend="Y: Divergance angle X: primordium", linestyle="", marker=".", color="r" )






if __name__ == "__main__":
    m = DiscInhibitorPhyllotaxisModel( visualisation=1 )
    m.c_discretization =100
    m.c_prim_size = 2.1
    m.run(nbr_prim=100)

#m.visualise_time_diff()
#import pickle
#prim_stable = pickle.load(open("prim1.4-3.5-0.2--2000.pickle"))
#
##psyco.full()            
#ang = {}
#tim = {}
#prim = {}
#a =prim_stable.keys()
#print a
#for i in a:
#    m = DiscInhibitorPhyllotaxisModel(prims=prim_stable[ i ])
#    print "calculating for: ", i
#    m.c_prim_size = i
#    m.run(nbr_prim=100)
#    ang[ i ]= m.i_prim2init_pos.copy()
#    tim[ i ]= m.i_prim2time.copy()
#    prim[ i ] =m.prims.copy()
#import pickle
#pickle.dump(ang, open("ang1.4-3.5-0.2-2000.pickle","w" ))
#pickle.dump(tim, open("tim1.4-3.5-0.2-2000.pickle","w" ))
#pickle.dump(prim, open("prim1.4-3.5-0.2--2000.pickle","w" ))
#ang = pickle.load(open("ang1.4-3.5-0.2-2000.pickle"))
#tim = pickle.load(open("tim1.4-3.5-0.2-2000.pickle"))
