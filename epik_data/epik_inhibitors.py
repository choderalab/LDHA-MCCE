#!/usr/bin/env python

"""Run epik on all substrates, products and cofactors."""

import os
import re
import csv
import traceback
import numpy as np
import logging
from openeye import oechem
from openmoltools import openeye, schrodinger

MAX_ENERGY_PENALTY = 10.0 # kT

def read_molecules(filename):
    """Read a file into an OpenEye molecule (or list of molecules).

    Parameters
    ----------
    filename : str
        The name of the file to read (e.g. mol2, sdf)

    Returns
    -------
    molecule : openeye.oechem.OEMol
        The OEMol molecule read, or a list of molecules if multiple molecules are read.
        If no molecules are read, None is returned.

    """

    ifs = oechem.oemolistream(filename)
    molecules = list()
    for mol in ifs.GetOEMols():
        mol_copy = oechem.OEMol(mol)
        molecules.append(mol_copy)
    ifs.close()

    if len(molecules) == 0:
        return None
    elif len(molecules) == 1:
        return molecules[0]
    else:
        return molecules

def DumpSDData(mol):
    logging.info(("SD data of", mol.GetTitle()))
    #loop over SD data
    for dp in oechem.OEGetSDDataPairs(mol):
        logging.info((dp.GetTag(), ':', dp.GetValue()))
    logging.info()

def retrieve_url(url, filename):
    import urllib.request, urllib.error, urllib.parse
    logging.info(url)
    response = urllib.request.urlopen(url)
    html = response.read()
    outfile = open(filename, 'wb')
    outfile.write(html)
    outfile.close()

def read_molecule(filename):
    ifs = oechem.oemolistream()
    ifs.open(filename)
    molecule = oechem.OEMol()
    oechem.OEReadMolecule(ifs, molecule)
    ifs.close()
    return molecule

def fix_mol2_resname(filename, residue_name):
    # Replace <0> substructure names with residue name.
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()
    newlines = [line.replace('<0>', residue_name) for line in lines]
    outfile = open(filename, 'w')
    outfile.writelines(newlines)
    outfile.close()

def write_mol2_preserving_atomnames(filename, molecules, residue_name):
    ofs = oechem.oemolostream()
    ofs.open(filename)
    ofs.SetFlavor(oechem.OEFormat_MOL2, oechem.OEOFlavor_MOL2_GeneralFFFormat)
    try:
        for molecule in molecules:
            oechem.OEWriteMolecule(ofs, molecule)
    except:
        oechem.OEWriteMolecule(ofs, molecules)
    ofs.close()
    fix_mol2_resname(filename, residue_name)

def enumerate_conformations(name, pdbfile=None, smiles=None, pdbname=None, pH=7.4):
    """Run Epik to get protonation states using PDB residue templates for naming.

    Parameters
    ----------
    name : str
       Common name of molecule (used to create subdirectory)
    smiles : str
       Isomeric SMILES string
    pdbname : str
       Three-letter PDB code (e.g. 'DB8')
    """
    # Create output subfolder
    output_basepath = os.path.join(output_dir, name)
    if not os.path.isdir(output_basepath):
        os.mkdir(output_basepath)
    output_basepath = os.path.join(output_basepath, name)

    if pdbname:
        # Make sure to only use one entry if there are mutliple
        if ' ' in pdbname:
            pdbnames = pdbname.split(' ')
            logging.info(("Splitting '%s' into first entry only: '%s'" % (pdbname, pdbnames[0])))
            pdbname = pdbnames[0]

        # Retrieve PDB (for atom names)
        url = 'http://ligand-expo.rcsb.org/reports/%s/%s/%s_model.pdb' % (pdbname[0], pdbname, pdbname)
        pdb_filename = output_basepath + '-input.pdb'
        retrieve_url(url, pdb_filename)
        pdb_molecule = read_molecule(pdb_filename)

        # Retrieve SDF (for everything else)
        url = 'http://ligand-expo.rcsb.org/reports/%s/%s/%s_model.sdf' % (pdbname[0], pdbname, pdbname)
        sdf_filename = output_basepath + '-input.sdf'
        retrieve_url(url, sdf_filename)
        sdf_molecule = read_molecule(sdf_filename)

        # Replace atom names in SDF
        for (sdf_atom, pdb_atom) in zip(sdf_molecule.GetAtoms(), pdb_molecule.GetAtoms()):
            sdf_atom.SetName(pdb_atom.GetName())
        # Assign Tripos atom types
        oechem.OETriposAtomTypeNames(sdf_molecule)
        oechem.OETriposBondTypeNames(sdf_molecule)

        oe_molecule = sdf_molecule

        # We already know the residue name
        residue_name = pdbname
    elif smiles:
        # Generate molecule geometry with OpenEye
        logging.info(("Generating molecule {}".format(name)))
        oe_molecule = openeye.smiles_to_oemol(smiles)
        # Assign Tripos atom types
        oechem.OETriposAtomTypeNames(oe_molecule)
        oechem.OETriposBondTypeNames(oe_molecule)
        try:
            logging.info("Charging initial")
            write_mol2_preserving_atomnames(output_basepath + '-debug.mol2', oe_molecule, 'debug')
            oe_molecule = openeye.get_charges(oe_molecule, keep_confs=1)
        except RuntimeError as e:
            traceback.print_exc()
            logging.info(("Skipping molecule " + name))
            return
        residue_name = re.sub('[^A-Za-z]+', '', name.upper())[:3]
        logging.info("resname = %s", residue_name)
        oe_molecule.SetTitle(residue_name) # fix iupac name issue with mol2convert
    elif pdbfile:
        residue_name = re.sub('[^A-Za-z]+', '', name.upper())[:3]
        logging.info("Loading molecule molecule {0} from {1}".format(name, pdbfile))
        oe_molecule = read_molecule(pdbfile)
        # Assign Tripos atom types
        oechem.OETriposAtomTypeNames(oe_molecule)
        oechem.OETriposBondTypeNames(oe_molecule)
        try:
            logging.info("Charging initial")
            write_mol2_preserving_atomnames(output_basepath + '-debug.mol2', oe_molecule, 'debug')
            oe_molecule = openeye.get_charges(oe_molecule, keep_confs=1)
        except RuntimeError as e:
            traceback.print_exc()
            logging.info(("Skipping molecule " + name))
            return
    else:
        raise Exception('Must provide SMILES string or pdbname, or pdbfile')

    # Save mol2 file, preserving atom names
    logging.info(("Running epik on molecule {}".format(name)))
    mol2_file_path = output_basepath + '-input.mol2'
    write_mol2_preserving_atomnames(mol2_file_path, oe_molecule, residue_name)

    # Run epik on mol2 file
    mae_file_path = output_basepath + '-epik.mae'
    schrodinger.run_epik(mol2_file_path, mae_file_path, tautomerize=False,
                         max_structures=100, min_probability=np.exp(-MAX_ENERGY_PENALTY), ph=pH)

    logging.info("epik is done")
    # Convert maestro file to sdf and mol2
    output_sdf_filename = output_basepath + '-epik.sdf'
    output_mol2_filename = output_basepath + '-epik.mol2'
    # logging.info("Creating sdf")
    schrodinger.run_structconvert(mae_file_path, output_sdf_filename)
    # logging.info("Creating mol2")
    schrodinger.run_structconvert(mae_file_path, output_mol2_filename)

    # Read SDF file.
    ifs_sdf = oechem.oemolistream()
    ifs_sdf.SetFormat(oechem.OEFormat_SDF)
    ifs_sdf.open(output_sdf_filename)
    sdf_molecule = oechem.OEGraphMol()

    # Read MOL2 file.
    ifs_mol2 = oechem.oemolistream()
    ifs_mol2.open(output_mol2_filename)
    mol2_molecule = oechem.OEMol()

    # Assign charges.
    logging.info("now assigning charges")
    charged_molecules = list()
    index = 0
    while oechem.OEReadMolecule(ifs_sdf, sdf_molecule):
        oechem.OEReadMolecule(ifs_mol2, mol2_molecule)

        index += 1
        logging.info(("Charging molecule %d" % (index)))
        try:
            # Charge molecule.
            charged_molecule = openeye.get_charges(mol2_molecule, max_confs=800, strictStereo=False, normalize=True, keep_confs=None)
            logging.info("charged again")
            # Assign Tripos types
            oechem.OETriposAtomTypeNames(charged_molecule)
            oechem.OETriposBondTypeNames(charged_molecule)
            # Store tags.
            oechem.OECopySDData(charged_molecule, sdf_molecule)
            # Store molecule
            charged_molecules.append(charged_molecule)
        except Exception as e:
            logging.info(e)
            logging.info("Skipping protomer/tautomer because of failed charging.")

    # Clean up
    ifs_sdf.close()
    ifs_mol2.close()

    # Write state penalites.
    outfile = open(output_basepath + '-state-penalties.out', 'w')
    for (index, charged_molecule) in enumerate(charged_molecules):
        # Get Epik data.
        logging.info("Writing epik data for molecule %d", index)
        epik_Ionization_Penalty = float(oechem.OEGetSDData(charged_molecule, "r_epik_Ionization_Penalty"))
        epik_Ionization_Penalty_Charging = float(oechem.OEGetSDData(charged_molecule, "r_epik_Ionization_Penalty_Charging"))
        epik_Ionization_Penalty_Neutral = float(oechem.OEGetSDData(charged_molecule, "r_epik_Ionization_Penalty_Neutral"))
        epik_State_Penalty = float(oechem.OEGetSDData(charged_molecule, "r_epik_State_Penalty"))
        epik_Tot_Q = int(oechem.OEGetSDData(charged_molecule, "i_epik_Tot_Q"))

        outfile.write('%16.8f\n' % epik_State_Penalty)
    outfile.close()

    # Write as PDB
    charged_pdb_filename = output_basepath + '-epik-charged.pdb'
    ofs = oechem.oemolostream(charged_pdb_filename)
    flavor = oechem.OEOFlavor_PDB_CurrentResidues | oechem.OEOFlavor_PDB_ELEMENT | oechem.OEOFlavor_PDB_BONDS | oechem.OEOFlavor_PDB_HETBONDS | oechem.OEOFlavor_PDB_BOTH
    ofs.SetFlavor(oechem.OEFormat_PDB, flavor)
    for (index, charged_molecule) in enumerate(charged_molecules):
        # Fix residue names
        for atom in charged_molecule.GetAtoms():
            residue = oechem.OEAtomGetResidue(atom)
            residue.SetName(residue_name)
            oechem.OEAtomSetResidue(atom, residue)

        #oechem.OEWritePDBFile(ofs, charged_molecule, flavor)
        oechem.OEWriteMolecule(ofs, charged_molecule)
    ofs.close()

    # Write molecules as mol2.
    charged_mol2_filename = output_basepath + '-epik-charged.mol2'
    write_mol2_preserving_atomnames(charged_mol2_filename, charged_molecules, residue_name)


if __name__ == '__main__':


    # for ph in [4.0, 5.0, 6.0, 7.0, 7.4, 8.0, 9.0, 10.0]:
    for ph in [6.6, 7.4]:
        input_csv_file = 'ldha_ligands_and_cofactors.csv'
        output_dir = 'output_{}'.format(ph)
        import os
        
        os.environ['SCHRODINGER'] = 'C:\\Program Files\\Schrodinger2015-3'
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        # Create output directory
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        # Parse csv file in universal newline mode
        with open(input_csv_file, 'r') as csv_file:
            next(csv_file, None) # skip header
            for (name,smiles,Chem_ID) in csv.reader(csv_file):
                if name == "NADH":
                    enumerate_conformations(name, pdbfile="../NADH.pdb")
                elif name == "Alpha-ketoglutaric acid" :
                    enumerate_conformations(name, pdbfile="../akg.pdb")

