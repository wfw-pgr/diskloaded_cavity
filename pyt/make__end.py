import numpy as np

# ========================================================= #
# ===  make__end.py ( for superfish )                   === #
# ========================================================= #

def make__end():

    # ------------------------------------------------- #
    # --- [1] load parameters                       --- #
    # ------------------------------------------------- #

    import nkUtilities.load__constants as lcn
    cnfFile = "dat/parameter.conf"
    const = lcn.load__constants( inpFile=cnfFile )


    print()
    print( "[make__end.py] end_outFile :: {0} ".format( const["end_outFile"] ) )
    print()

    # ------------------------------------------------- #
    # --- [2] comment & settings                    --- #
    # ------------------------------------------------- #

    if ( const["auto_drive_point"] ):
        drive_x           = const["pipe_length"]
        drive_y           = const["cell_radius"]
        const["xy_drive"] = [ drive_x, drive_y ]
    
    comment = \
        "### {0} GHz Cavity\n"\
        "### disk-loaded cavity \n"\
        "### created by K.Nishida\n"\
        "###\n\n".format( const["frequency"]/1.0e9 )

    generals = \
        "kprob=1                                ! superfish problem \n"\
        "icylin=1                               ! cylindrical coordinates \n"\
        "conv={0}                               ! unit conversion ( e.g. cm => mm ) \n"\
        "freq={1}                               ! frequency (MHz) \n"\
        "dx={2}                                 ! mesh size \n"\
        "xdri={3[0]},ydri={3[1]}                ! drive point of RF \n"\
        "kmethod=1                              ! use beta to compute wave number \n"\
        "beta={4}                               ! Particle velocity for transit-time integrals \n"\
        .format( const["unit_conversion"], const["frequency"]/1.0e6, const["meshsize"], \
                 const["xy_drive"], const["beta"] )

    boundaries = \
        "nbsup={0}                              ! boundary :: upper  ( 0:Neumann, 1:Dirichlet )\n"\
        "nbslo={1}                              !          :: lower  \n"\
        "nbsrt={2}                              !          :: right  \n"\
        "nbslf={3}                              !          :: left   \n"\
        .format( const["boundary_upper"], const["boundary_lower"], \
                 const["boundary_right"], const["boundary_left"] )
        
    
    settings   = "&reg {0}{1}&\n\n".format( generals, boundaries )

    # ------------------------------------------------- #
    # --- [3] pillbox cavity geometry               --- #
    # ------------------------------------------------- #

    b          = const["cell_radius"]
    d          = const["cell_length"]
    a          = const["disk_radius"]
    t          = const["disk_length"]
    rp         = const["pipe_radius"]
    lp         = const["pipe_length"]
    hd         = 0.5 * d
    ht         = 0.5 * t

    #
    # -- ltype_== 1 :: straight line.
    # -- ltype_== 2 :: circle.
    # -- ltype_, x_, y_, x0_, y0_ -- #
    #
    pts        = [ [ 1,           0.0,  0.0,      0.0,  0.0 ],
                   [ 1,           0.0,   rp,      0.0,  0.0 ],
                   [ 1,         lp-ht,   rp,      0.0,  0.0 ],
                   [ 2,            ht,  0.0,    lp-ht,rp+ht ],
                   [ 1,            lp,    b,      0.0,  0.0 ],
                   [ 1,         lp+hd,    b,      0.0,  0.0 ],
                   [ 1,         lp+hd,  0.0,      0.0,  0.0 ],
                   [ 1,           0.0,  0.0,      0.0,  0.0 ], ]
    pts        = np.array( pts )

    ltype_, x_, y_, x0_, y0_  = 0, 1, 2, 3, 4 
    geometry   = ""
    for ik, pt in enumerate( pts ):
        if ( int( pt[ltype_] ) == 1 ):
            geometry += "$po x={0}, y={1} $\n".format( pt[x_], pt[y_] )
        if ( int( pt[ltype_] ) == 2 ):
            geometry += "$po nt=2, x={0}, y={1}, x0={2}, y0={3} $\n".format( pt[x_], pt[y_], pt[x0_], pt[y0_] )

        
    # ------------------------------------------------- #
    # --- [4] write in a file                       --- #
    # ------------------------------------------------- #

    with open( const["end_outFile"], "w" ) as f:
        f.write( comment  )
        f.write( settings )
        f.write( geometry )


    return()




# ========================================================= #
# ===  make in7 ( input file for sf7 )                  === #
# ========================================================= #

def make__in7():

    # -- execute this script to generate grided field -- #
    # -- sf7 : post processor for poisson-superfish   -- #
    # -- in7 : input file for sf7                     -- #

    # ------------------------------------------------- #
    # --- [1] load config file                      --- #
    # ------------------------------------------------- #

    import nkUtilities.load__constants as lcn
    cnfFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnfFile )

    if ( const["flag__auto_in7"] ):
        xMax                    = const["pipe_length"] + const["cell_length"] * 0.5
        yMax                    = const["pipe_radius"]
        const["in7_xMinMaxNum"] = [0.0,xMax,const["in7_auto_LI"]]
        const["in7_yMinMaxNum"] = [0.0,yMax,const["in7_auto_LJ"]]
    
    # ------------------------------------------------- #
    # --- [2] write in file                         --- #
    # ------------------------------------------------- #
    
    line1 = "rect noscreen\n"
    line2 = "{0} {1} {2} {3}\n".format( const["in7_xMinMaxNum"][0], const["in7_yMinMaxNum"][0], \
                                        const["in7_xMinMaxNum"][1], const["in7_yMinMaxNum"][1]  )
    line3 = "{0} {1}\n".format( int( const["in7_xMinMaxNum"][2]-1 ), \
                                int( const["in7_yMinMaxNum"][2]-1 ) )
    line4 = "end\n"
    # line3 :: number of space should be prescribed == Not number of nodes.

    text  = line1 + line2 + line3 + line4

    with open( const["end_in7File"], "w" ) as f:
        f.write( text )
    print( "[make__in7.py] outFile :: {0} ".format( const["end_in7File"] ) )




# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    make__end()
    make__in7()
