####################################
# Topology File for:
# param/AKG.tpl
# Alpha-ketoglutaric-acid
#
# Created on: 2016-09-11
#
# Created with: make_tpl_1.py by Salah Salah
####################################

# neural always starts with 0
# numberical value means the charge is 1
# alphabet lower case means the charge is 2
# alphabet upper case means the charge is 3
# nothing for charge of 4, this code will not work

CONFLIST AKG        AKGBK AKG-a AKG-1 AKGDM 

NATOM    AKGBK      0
NATOM    AKG-a      14
NATOM    AKG-1      15
NATOM    AKGDM      0

IATOM    AKG-a    C1    0
IATOM    AKG-a    C2    1
IATOM    AKG-a    C3    2
IATOM    AKG-a    O1    3
IATOM    AKG-a    O2    4
IATOM    AKG-a    C4    5
IATOM    AKG-a    O3    6
IATOM    AKG-a    C5    7
IATOM    AKG-a    O4    8
IATOM    AKG-a    O5    9
IATOM    AKG-a    H1   10
IATOM    AKG-a    H2   11
IATOM    AKG-a    H3   12
IATOM    AKG-a    H4   13

IATOM    AKG-1    C1    0
IATOM    AKG-1    C2    1
IATOM    AKG-1    C3    2
IATOM    AKG-1    O1    3
IATOM    AKG-1    O2    4
IATOM    AKG-1    C4    5
IATOM    AKG-1    O3    6
IATOM    AKG-1    C5    7
IATOM    AKG-1    O4    8
IATOM    AKG-1    O5    9
IATOM    AKG-1    H1   10
IATOM    AKG-1    H2   11
IATOM    AKG-1    H3   12
IATOM    AKG-1    H4   13
IATOM    AKG-1    H5   14

ATOMNAME AKG-a     0  C1
ATOMNAME AKG-a     1  C2
ATOMNAME AKG-a     2  C3
ATOMNAME AKG-a     3  O1
ATOMNAME AKG-a     4  O2
ATOMNAME AKG-a     5  C4
ATOMNAME AKG-a     6  O3
ATOMNAME AKG-a     7  C5
ATOMNAME AKG-a     8  O4
ATOMNAME AKG-a     9  O5
ATOMNAME AKG-a    10  H1
ATOMNAME AKG-a    11  H2
ATOMNAME AKG-a    12  H3
ATOMNAME AKG-a    13  H4

ATOMNAME AKG-1     0  C1
ATOMNAME AKG-1     1  C2
ATOMNAME AKG-1     2  C3
ATOMNAME AKG-1     3  O1
ATOMNAME AKG-1     4  O2
ATOMNAME AKG-1     5  C4
ATOMNAME AKG-1     6  O3
ATOMNAME AKG-1     7  C5
ATOMNAME AKG-1     8  O4
ATOMNAME AKG-1     9  O5
ATOMNAME AKG-1    10  H1
ATOMNAME AKG-1    11  H2
ATOMNAME AKG-1    12  H3
ATOMNAME AKG-1    13  H4
ATOMNAME AKG-1    14  H5

#1.Basic Conformer Information: name, pka, em, rxn.
#23456789A123456789B123456789C

# PROTON SECTION: PROTON means charge

PROTON   AKG-a      0    
PROTON   AKG-1      0    
PROTON   AKGDM      0    

# Solution pKa Section: pKa data from CRC Handbook of Chemistry and Physics
# pka is set to zero
PKA      AKG-a         0.000
PKA      AKG-1         0.000
PKA      AKGDM         0.000

#ELECTRON SECTION:
ELECTRON AKG-a      0.0  
ELECTRON AKG-1      0.0  
ELECTRON AKGDM      0.0  

# EM SECTION:
EM       AKG-a      0.0  
EM       AKG-1      0.0  
EM       AKGDM      0.0  


# REACTION FIELD ENERGY SECTION:
RXN      AKG-a      -51.423  
RXN      AKG-1      -21.296

#  AKG-a
#ONNECT   conf atom  orbital  ires conn ires conn ires conn ires conn 
#ONNECT |-----|----|---------|----|----|----|----|----|----|----|----|----|----|
CONNECT  AKG-a  C1     sp3     0    C2   0    C4   0    H1   0    H2  
CONNECT  AKG-a  C2     sp3     0    C1   0    C3   0    H3   0    H4  
CONNECT  AKG-a  C3     sp2     0    C2   0    O1   0    O2  
CONNECT  AKG-a  O1   unknown   0    C3  
CONNECT  AKG-a  O2   unknown   0    C3  
CONNECT  AKG-a  C4     sp2     0    C1   0    O3   0    C5  
CONNECT  AKG-a  O3     sp2     0    C4  
CONNECT  AKG-a  C5     sp2     0    C4   0    O4   0    O5  
CONNECT  AKG-a  O4   unknown   0    C5  
CONNECT  AKG-a  O5   unknown   0    C5  
CONNECT  AKG-a  H1      s      0    C1  
CONNECT  AKG-a  H2      s      0    C1  
CONNECT  AKG-a  H3      s      0    C2  
CONNECT  AKG-a  H4      s      0    C2  

#  AKG-1
#ONNECT   conf atom  orbital  ires conn ires conn ires conn ires conn 
#ONNECT |-----|----|---------|----|----|----|----|----|----|----|----|----|----|
CONNECT  AKG-1  C1     sp3     0    C2   0    C4   0    H1   0    H2  
CONNECT  AKG-1  C2     sp3     0    C1   0    C3   0    H3   0    H4  
CONNECT  AKG-1  C3     sp2     0    C2   0    O1   0    O2  
CONNECT  AKG-1  O1     sp2     0    C3  
CONNECT  AKG-1  O2     sp3     0    C3   0    H5  
CONNECT  AKG-1  C4     sp2     0    C1   0    O3   0    C5  
CONNECT  AKG-1  O3     sp2     0    C4  
CONNECT  AKG-1  C5     sp2     0    C4   0    O4   0    O5  
CONNECT  AKG-1  O4   unknown   0    C5  
CONNECT  AKG-1  O5   unknown   0    C5  
CONNECT  AKG-1  H1      s      0    C1  
CONNECT  AKG-1  H2      s      0    C1  
CONNECT  AKG-1  H3      s      0    C2  
CONNECT  AKG-1  H4      s      0    C2  
CONNECT  AKG-1  H5      s      0    O2  

# Atom Parameters:
# Van Der Waals Radii. See source for reference
RADIUS   AKG    C1        1.7
RADIUS   AKG    C2        1.7
RADIUS   AKG    C3        1.7
RADIUS   AKG    O1       1.52
RADIUS   AKG    O2       1.52
RADIUS   AKG    C4        1.7
RADIUS   AKG    O3       1.52
RADIUS   AKG    C5        1.7
RADIUS   AKG    O4       1.52
RADIUS   AKG    O5       1.52
RADIUS   AKG    H1        1.2
RADIUS   AKG    H2        1.2
RADIUS   AKG    H3        1.2
RADIUS   AKG    H4        1.2
RADIUS   AKG    H5        1.2

CHARGE   AKG-a  C1   -0.157
CHARGE   AKG-a  C2  -0.1747
CHARGE   AKG-a  C3   0.9037
CHARGE   AKG-a  O1  -0.8769
CHARGE   AKG-a  O2  -0.8769
CHARGE   AKG-a  C4   0.4534
CHARGE   AKG-a  O3  -0.5966
CHARGE   AKG-a  C5   0.8252
CHARGE   AKG-a  O4  -0.8374
CHARGE   AKG-a  O5  -0.8374
CHARGE   AKG-a  H1   0.0654
CHARGE   AKG-a  H2   0.0654
CHARGE   AKG-a  H3   0.0219
CHARGE   AKG-a  H4   0.0219

CHARGE   AKG-1  C1  -0.2006
CHARGE   AKG-1  C2   -0.102
CHARGE   AKG-1  C3    0.646
CHARGE   AKG-1  O1  -0.5437
CHARGE   AKG-1  O2  -0.6322
CHARGE   AKG-1  C4   0.4457
CHARGE   AKG-1  O3  -0.5537
CHARGE   AKG-1  C5   0.8437
CHARGE   AKG-1  O4   -0.805
CHARGE   AKG-1  O5   -0.805
CHARGE   AKG-1  H1   0.0733
CHARGE   AKG-1  H2   0.0733
CHARGE   AKG-1  H3   0.0666
CHARGE   AKG-1  H4   0.0666
CHARGE   AKG-1  H5    0.427

# EXTRA energy for tautomers:
EXTRA    AKG-a         0.000
EXTRA    AKG-1         4.545

