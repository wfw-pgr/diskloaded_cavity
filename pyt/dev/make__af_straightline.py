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
        const["xy_drive"] = [ 0.0, const["disk_radius"] ]
    
    comment = \
        "### {0} GHz Cavity\n"\
        "### disk-loaded cavity \n"\
        "### created by K.Nishida\n"\
        "###\n\n".format( const["frequency"]/1.0e9 )

    settings = \
        "&reg kprob=1                           ! superfish problem \n"\
        "icylin=1                               ! cylindrical coordinates \n"\
        "conv={0}                               ! unit conversion ( e.g. cm => mm ) \n"\
        "freq={1}                               ! frequency (MHz) \n"\
        "dx={2}                                 ! mesh size \n"\
        "xdri={3[0]},ydri={3[1]}                ! drive point of RF \n"\
        "kmethod=1                              ! use beta to compute wave number \n"\
        "beta={4} &                             ! Particle velocity for transit-time integrals \n"\
        "\n\n".format( const["unit_conversion"], const["frequency"]/1.0e6, const["meshsize"], \
                       const["xy_drive"], const["beta"] )

    # ------------------------------------------------- #
    # --- [3] pillbox cavity geometry               --- #
    # ------------------------------------------------- #

    b          = const["cell_radius"]
    d          = const["cell_length"]
    a          = const["disk_radius"]
    t          = const["disk_length"]
    hd         = 0.5 * d
    ht         = 0.5 * t

    pts        = [ [           0.0,  0.0 ],
                   [           0.0,    b ],
                   [         hd-ht,    b ],
                   [         hd-ht,    a ],
                   [         hd+ht,    a ],
                   [         hd+ht,    b ],
                   [     d + hd-ht,    b ],
                   [     d + hd-ht,    a ],
                   [     d + hd+ht,    a ],
                   [     d + hd+ht,    b ],
                   [ 2.0*d + hd-ht,    b ],
                   [ 2.0*d + hd-ht,    a ],
                   [ 2.0*d + hd+ht,    a ],
                   [ 2.0*d + hd+ht,    b ],
                   [ 3.0*d        ,    b ],
                   [ 3.0*d        ,  0.0 ],
                   [           0.0,  0.0 ], ]
    pts        = np.array( pts )

    x_, y_     = 0, 1
    geometry   = ""
    for ik, pt in enumerate( pts ):
        geometry += "$po x={0}, y={1} $\n".format( pt[x_], pt[y_] )

        
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
