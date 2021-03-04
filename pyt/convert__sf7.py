import sys
import numpy                      as np
import nkUtilities.load__config   as lcf
import nkUtilities.cMapTri        as cmt
import nkUtilities.configSettings as cfs


# ========================================================= #
# ===  convert__sf7.py                                  === #
# ========================================================= #

def convert__sf7():

    # ------------------------------------------------- #
    # --- [1] load config & sf7 file                --- #
    # ------------------------------------------------- #

    import nkUtilities.load__constants as lcn
    cnfFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnfFile )
    
    with open( const["sf7File"], "r" ) as f:
        lines = f.readlines()

    # ------------------------------------------------- #
    # --- [2] search for the data start line        --- #
    # ------------------------------------------------- #

    if ( const["flag__auto_in7"] ):
        LI, LJ, LK = int( const["in7_auto_LI"] ), int( const["in7_auto_LJ"] ), 1
    else:
        LI, LJ, LK = int( const["in7_xMinMaxNum"][2] ), int( const["in7_yMinMaxNum"][2] ), 1
    nLine      = LI*LJ*LK
    searchline = "Electromagnetic fields for a rectangular area with corners at:"
    offset     = 7
    DataStart  = None
    for iL,line in enumerate(lines):
        if ( line.strip() == searchline ):
            DataStart = iL + offset
            break
    if ( DataStart is None ):
        sys.exit( "[convert__sf7.py] cannot find searchline in {0}".format( const["sf7File"] ) )
        
    # ------------------------------------------------- #
    # --- [3] fetch Data from outsf7.txt            --- #
    # ------------------------------------------------- #
    
    # -- [3-1] load file contents                   --  #
    with open( const["sf7File"], "r" ) as f:
        Data = np.loadtxt( f, skiprows=DataStart, max_rows=nLine )
    wData = np.zeros( (Data.shape[0],7) )
        
    # -- [3-2] unit conversion                      --  #
    wData[:,0] = Data[:,0] * 1.e-3 #  Z  :: (mm)   -> (m)
    wData[:,1] = Data[:,1] * 1.e-3 #  R  :: (mm)   -> (m)
    wData[:,2] = Data[:,0] * 0.0   #  z-coordinate
    wData[:,3] = Data[:,2] * 1.e+6 #  Ez :: (MV/m) -> (V/m)
    wData[:,4] = Data[:,3] * 1.e+6 #  Er :: (MV/m) -> (V/m)
    wData[:,5] = Data[:,4] * 1.e+6 # |E| :: (MV/m) -> (V/m)
    wData[:,6] = Data[:,5]         #  H  :: (A/m)
    
    # ------------------------------------------------- #
    # --- [4] save as a pointData                   --- #
    # ------------------------------------------------- #

    wData_ = np.reshape( wData, (LK,LJ,LI,7) )
    
    import nkUtilities.save__pointFile as spf
    names = ["xp","yp","zp","Ez","Er","|E|","Hp"]
    spf.save__pointFile( outFile=const["spfFile"], Data=wData_, names=names )


    # ------------------------------------------------- #
    # --- [5] convert into field-type pointFile     --- #
    # ------------------------------------------------- #
    #
    #  x => r direction
    #  y => t direction
    #
    #  -- [5-1] EField    -- #
    xp_, yp_, zp_  = 0, 1, 2
    ex_, ey_, ez_  = 3, 4, 5
    
    pData          = np.zeros( (wData.shape[0],6) )
    pData[:,xp_]   = wData[:,1]
    pData[:,yp_]   = 0.0
    pData[:,zp_]   = wData[:,0]
    pData[:,ex_]   = wData[:,4]
    pData[:,ey_]   = 0.0
    pData[:,ez_]   = wData[:,3]

    index          = np.lexsort( ( pData[:,xp_], pData[:,yp_], pData[:,zp_]) )
    pData          = pData[index]
    pData          = np.reshape( pData, (LI,1,LJ,6) )
    
    import nkUtilities.save__pointFile as spf
    names = ["xp","yp","zp","Ex","Ey","Ez"]
    spf.save__pointFile( outFile=const["efieldFile"], Data=pData, names=names )

    #  -- [5-2] BField    -- #

    xp_, yp_, zp_  = 0, 1, 2
    bx_, by_, bz_  = 3, 4, 5
    
    pData          = np.zeros( (wData.shape[0],6) )
    pData[:,xp_]   = wData[:,1]
    pData[:,yp_]   = 0.0
    pData[:,zp_]   = wData[:,0]
    pData[:,bx_]   = 0.0
    pData[:,by_]   = wData[:,6] * const["mu0"]
    pData[:,bz_]   = 0.0

    index          = np.lexsort( ( pData[:,xp_], pData[:,yp_], pData[:,zp_]) )
    pData          = pData[index]
    pData          = np.reshape( pData, (LI,1,LJ,6) )
    
    import nkUtilities.save__pointFile as spf
    names = ["xp","yp","zp","Bx","By","Bz"]
    spf.save__pointFile( outFile=const["bfieldFile"], Data=pData, names=names )

    

# ========================================================= #
# ===  display__sf7                                     === #
# ========================================================= #
def display__sf7():
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnfFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnfFile )

    config  = lcf.load__config()
    datFile =   const["spfFile"]
    pngFile = ( const["spfFile"].replace( "dat", "png" ) ).replace( ".png", "_{0}.png" )

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data  = lpf.load__pointFile( inpFile=datFile, returnType="point" )
    xAxis = Data[:,0]
    yAxis = Data[:,1]
    zAxis = Data[:,2]
    Ez    = Data[:,3]
    Er    = Data[:,4]
    Ea    = Data[:,5]
    Hp    = Data[:,6]
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="cMap_def", config=config )
    config["FigSize"]        = (8,3)
    config["cmp_position"]   = [0.16,0.12,0.97,0.88]
    config["xTitle"]         = "Z (m)"
    config["yTitle"]         = "R (m)"
    config["xMajor_Nticks"]  = 8
    config["yMajor_Nticks"]  = 3
    config["cmp_xAutoRange"] = True
    config["cmp_yAutoRange"] = True
    config["cmp_xRange"]     = [-5.0,+5.0]
    config["cmp_yRange"]     = [-5.0,+5.0]
    config["vec_AutoScale"]    = True
    config["vec_AutoRange"]    = True
    config["vec_AutoScaleRef"] = 200.0
    config["vec_nvec_x"]       = 24
    config["vec_nvec_y"]       = 6
    config["vec_interpolation"] = "nearest"

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=Ez, pngFile=pngFile.format( "Ez" ), config=config )
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=Er, pngFile=pngFile.format( "Er" ), config=config )
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=Ea, pngFile=pngFile.format( "Ea" ), config=config )
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=Hp, pngFile=pngFile.format( "Hp" ), config=config )
    
    fig = cmt.cMapTri( pngFile=pngFile.format( "Ev" ), config=config )
    fig.add__contour( xAxis=xAxis, yAxis=yAxis, Cntr=Hp )
    fig.add__cMap   ( xAxis=xAxis, yAxis=yAxis, cMap=Hp )
    fig.add__vector ( xAxis=xAxis, yAxis=yAxis, uvec=Ez, vvec=Er, color="blue" )
    fig.save__figure()
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    convert__sf7()
    display__sf7()
