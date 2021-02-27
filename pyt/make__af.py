import numpy as np

# ========================================================= #
# ===  make__af.py ( for superfish )                    === #
# ========================================================= #

def make__af():

    # ------------------------------------------------- #
    # --- [1] load parameters                       --- #
    # ------------------------------------------------- #

    import nkUtilities.load__constants as lcn
    cnfFile = "dat/parameter.conf"
    const = lcn.load__constants( inpFile=cnfFile )


    print()
    print( "[make__af.py] outFile :: {0} ".format( const["outFile"] ) )
    print()

    # ------------------------------------------------- #
    # --- [2] comment & settings                    --- #
    # ------------------------------------------------- #

    if ( const["auto_drive_point"] ):
        const["xy_drive"] = [ 0.0, const["cell_radius"] ]
    
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
    hd         = 0.5 * d
    ht         = 0.5 * t

    #
    # -- ltype_== 1 :: straight line.
    # -- ltype_== 2 :: circle.
    # -- ltype_, x_, y_, x0_, y0_ -- #
    #
    pts        = [ [ 1,           0.0,  0.0,      0.0,  0.0 ],
                   [ 1,           0.0,    b,      0.0,  0.0 ],
                   [ 1,         hd-ht,    b,      0.0,  0.0 ],
                   [ 1,         hd-ht, a+ht,      0.0,  0.0 ],
                   [ 2,           +ht,  0.0,       hd, a+ht ],
                   [ 1,         hd+ht,    b,      0.0,  0.0 ],
                   [ 1,     d + hd-ht,    b,      0.0,  0.0 ],
                   [ 1,     d + hd-ht, a+ht,      0.0,  0.0 ],
                   [ 2,           +ht,  0.0,     d+hd, a+ht ],
                   [ 1,     d + hd+ht,    b,      0.0,  0.0 ],
                   [ 1, 2.0*d + hd-ht,    b,      0.0,  0.0 ],
                   [ 1, 2.0*d + hd-ht, a+ht,      0.0,  0.0 ],
                   [ 2,           +ht,  0.0, 2.0*d+hd, a+ht ],
                   [ 1, 2.0*d + hd+ht,    b,      0.0,  0.0 ],
                   [ 1, 3.0*d        ,    b,      0.0,  0.0 ],
                   [ 1, 3.0*d        ,  0.0,      0.0,  0.0 ],
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

    with open( const["outFile"], "w" ) as f:
        f.write( comment  )
        f.write( settings )
        f.write( geometry )


    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    make__af()
