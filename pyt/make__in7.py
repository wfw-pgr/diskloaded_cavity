
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
        const["in7_xMinMaxNum"] = [0.0,3.0*const["cell_length"],const["in7_auto_LI"]]
        const["in7_yMinMaxNum"] = [0.0,    const["disk_radius"],const["in7_auto_LJ"]]
    
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

    with open( const["in7File"], "w" ) as f:
        f.write( text )
    print( "[make__in7.py] outFile :: {0} ".format( const["in7File"] ) )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    make__in7()
        
