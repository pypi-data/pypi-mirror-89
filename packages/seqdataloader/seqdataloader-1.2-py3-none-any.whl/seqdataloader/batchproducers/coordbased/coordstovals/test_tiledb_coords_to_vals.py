#tests for class seqdataloader.batchproducers.coordbased.coordstovals.BasicTiledbProfileCoordsToVals
import pdb 
from seqdataloader.batchproducers.coordbased.coordstovals import *
from collections import namedtuple

tiledb_paths="/mnt/data/tiledb/encode/dnase/ENCSR000EOY"
pos_label_source_attribute="fc_bigwig"
neg_label_source_attribute="fc_bigwig"

Coord=namedtuple('Coord','chrom','start','end','isplusstrand')
coords=[Coord('chr1',1000000,2000000,True),
        Coord('chr2',1000000,2000000,True),
        Coord('chr3',1000000,2000000,True),
        Coord('chr4',1000000,2000000,True),
        Coord('chr5',1000000,2000000,True),
        Coord('chr6',1000000,2000000,True),
        Coord('chr7',1000000,2000000,True),
        Coord('chr1',1000000,2000000,False),
        Coord('chr2',1000000,2000000,False),
        Coord('chr3',1000000,2000000,False),
        Coord('chr4',1000000,2000000,False),
        Coord('chr5',1000000,2000000,False),
        Coord('chr6',1000000,2000000,False),
        Coord('chr7',1000000,2000000,False)]

ctov=BasicTiledbProfileCoordsToVals(tiledb_paths=tiledb_paths,
                                    pos_label_source_attribute=pos_label_source_attribute,
                                    neg_label_source_attribute=neg_label_source_attribute)
print("made coordstovals object")
vals=ctov.__call__(coords)
pdb.set_trace()
