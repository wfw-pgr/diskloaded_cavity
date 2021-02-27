import os, sys
import numpy as np

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
    
    LI, LJ, LK = int( const["sf7_xMinMaxNum"][2] ), int( const["sf7_yMinMaxNum"][2] ), 1
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
    spf.save__pointFile( outFile=const["efdFile"], Data=wData_, names=names )


    # ------------------------------------------------- #
    # --- [5] convert into field-type pointFile     --- #
    # ------------------------------------------------- #
    #
    #  x => r direction
    #  y => t direction
    #
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
    spf.save__pointFile( outFile=const["fieldFile"], Data=pData, names=names )
    
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    convert__sf7()
