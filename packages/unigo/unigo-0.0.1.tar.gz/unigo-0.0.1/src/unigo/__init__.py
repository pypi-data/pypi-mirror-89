from .tree import setOntology, createGoTree
from . import stat_utils

"""
Minimal ontology tree of a uniprot collection

Merging Uniprot Object Collection 
Consrtuctor

"""

def prune(unigoObj, predicate):
    """Create a Unigo object by Pruning the supplied Unigo instance

        Parameters
        ----------
        unigoObj : 
        predicate: predicate function applied to prodived Unigo to drop or keep its elements
    """
    _tree          = unigoObj.tree.drop(predicate)
    _tree_universe = unigoObj.tree_universe.drop(predicate)
    return Unigo( previous=(_tree, _tree_universe) )


def chop(unigoObj, name=None, ID=None):
    """Create a Unigo object with its root extracted from the provided Unigo instance

        Parameters
        ----------
        unigoObj : 
        name: name of the node the look for in provided unigoObj. It will be the root of the returned Unigo
        ID: ID of the node the look for in provided unigoObj. It will be the root of the returned Unigo
    """
    _tree          = unigoObj.tree.newRoot(predicate)
    _tree_universe = unigoObj.tree_universe.newRoot(predicate)
    return Unigo( previous=(_tree, _tree_universe) )

class Unigo:
    def __init__(self, previous=None, backgroundUniColl=None, proteinList=None, owlFile=None, ns="biological process"):#, **kwargs):
        """Create a Unigo object

        Parameters
        ----------
        owlFile : path to the ontology owl file.
        backgroundUniColl : collection of uniprot objects, defining the background population
        proteinList : A list of uniprot identifiers
        [Options]
        ns : a subset of ontology, default:biological process

        TODO: Check if all protein list are members of bkgUniCol

        """
        if previous:
            self.tree, self.tree_universe = previous
            return
        
        if backgroundUniColl is None or  proteinList is None:
            raise ValueError(f"parameters backgroundUniColl and proteinList are required")
        try :
            if owlFile is None:
                print("Fetching ontology")
                setOntology(url="http://purl.obolibrary.org/obo/go.owl")#, **kwargs)
            else:
                setOntology(owlFile=f"{os.path(__file__)}/default_ontology/go.owl")
        except Exception as e:
            print(f"Could not create ontology")
            print(e)
        
        self.tree = createGoTree(          ns       = ns,
                                  proteinList       = proteinList, 
                                  uniprotCollection = backgroundUniColl)

        proteinUniverseList = [ k for k in backgroundUniColl.keys() ]
        self.tree_universe = createGoTree(                ns = ns, 
                                           proteinList       = proteinUniverseList, 
                                           uniprotCollection = backgroundUniColl)

    def walk(self, type=None):
        """Iterate over the tree, by default the experimental one"""
        if type is None:
            for node in self.tree.walk():
                yield node
    
# Define rich view of stat results for notebook ?
def dumpStat():
    pass

#import json

#res = {}

#for node in goTreeObjExp.walk():
#    if node.pvalue:
#         res[ node.name ] = {
#             "name"          : node.name,
#             "pvalue"        : node.pvalue,
#             "proteineTotal" : node.getMembers(nr=True),
#             "proteineSA"    : list ( set (saList) & set(node.getMembers(nr=True)) )
#         }
        
#with open('TP_ORA.json', 'w') as fp:
#    json.dump(res, fp)
#res