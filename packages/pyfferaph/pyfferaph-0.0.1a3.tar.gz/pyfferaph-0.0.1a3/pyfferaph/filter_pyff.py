import argparse
import networkx as nx
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import MDAnalysis as mda
import logging as log
import json
import pathlib
import os
from collections import defaultdict



def macroIIN_generator(matrices_list, p_crit, out_file):

    ''' returns a macro interaction network containing
    all the instances from each network in
    matrices list with a value greater than p_crit '''

    nice_matrices = [np.loadtxt(m) for m in matrices_list]

    boolmats = [i > p_crit for i in nice_matrices]
    macroIIN = boolmats[0]

    for i in range (1,len(boolmats)):
        macroIIN = np.logical_or(macroIIN, boolmats[i])
    #print(qualcosa)
    np.savetxt(out_file, macroIIN)

    return macroIIN

def network_generator(network_matrix, topology_file):

    ''' returns a graph G based on the adjacency
    network_matrix. Each node in the graph is
    named after the corrisponding residue in
    the topology_file '''

    u = mda.Universe(topology_file)
    G = nx.Graph(network_matrix)
    identifiers = ["%s%d" % (r.resname,r.resnum) for r in u.residues]
    #print(identifiers)
    node_names = dict(zip(range(0,network_matrix.shape[0]),identifiers))
    #print(node_names)
    nx.relabel_nodes(G, node_names, copy=False)

    return G

def shortest_paths(G, source, target):

    ''' Returns all shorteset paths found
    in network G connecting source and target '''

    try:
        nx.shortest_path(G,source,target)
    except:
        print('no path between {} and {}'.format(source, target))
        print('\n')
        return None

    paths = [k for k in nx.all_shortest_paths(G,source,target)]

    return paths


def path_scores(paths):

    ''' Returns a dictionary with the following structure {'path':score}.
    A score is assigned to each path in paths; the score
    is computed summing the frequencies, calculated over all the
    paths connecting source and target, of each residue in the path '''

    frequency = dict()
    for path in paths:
        for position in range(len(path)):
            if path[position] not in frequency:
                frequency[path[position]] = 1
            else:
                frequency[path[position]] += 1
    #print(frequency)

    scores = dict()
    for path in paths:
        path_score = sum(frequency[i] for i in path)
        scores[str(path)] = path_score

    return scores


def communication_robustness(paths, threshold):

    ''' returns the communication robustness (cr) index
    for the pathway (list of paths) source-target (s-t) as:
    cr(s-t) = (paths s-t) * threshold / lenght_shortest_path '''

    n = len(paths)
    l = len(paths[0])
    cr = round(n*threshold/(l*100), 2)

    return cr


def selective_betweenness(G, source, target, sb_residue):

    ''' returns the selective betweenness value for
    sb_residue computed over all the shortest path
    connecting source and target in G '''

    paths = [k for k in nx.all_shortest_paths(G,source,target)]

    sb = 0
    for path in paths:
        #print(path)
        if sb_residue in path:
            sb += 1
    sb = round(sb / len(paths), 2)
    print(f'source: {source} target: {target}\nselective betweenness for {sb_residue}: {sb}')
    return sb


def all_shortest_paths(G, source_res, target_res, threshold):

    ''' prints to file all shortest paths in netework G connecting each
    source-target residues pair in source_res and target_res.
    A score is assigned to each path; the corresponding cr
    index is assigned to each pathway '''

    folder = create_directory()
    for res in source_res:
        file_name = f"{folder}/{res}.dat"
        lines = 0
        with open(file_name, 'w') as paths_file:
            for int_res in target_res:
                paths = shortest_paths(G, res, int_res)
                #print(paths)
                cr_index = communication_robustness(paths, threshold)
                #print(cr_index)
                scores = path_scores(paths)
                max_score = max(scores.values())
                best_paths = []
                #print(scores)
                path_info = f'source node:\t{res}\ntarget node:\t{int_res}\n'
                paths_file.write(path_info)
                paths_file.write(f'cr value:\t{str(cr_index)}\n')
                paths_file.write(f'Number of shortest paths:\t{len(paths)}\n')
                if paths != None:
                    paths_file.write(f'Length of the shortest paths:\t{len(paths[0])}\n\n')
                    path_i = 0
                    for path in paths:
                        path_i += 1
                        lines += 1
                        paths_file.write(f'Path\t{path_i}:\n{str(path)}\n')
                        score = scores[str(path)]
                        #print(score)
                        if score == max_score:
                            best_paths.append(path)
                        paths_file.write(f'score\t{str(score)}\n\n')
                    paths_file.write(f'Best shortest paths (score {max_score}):\n')
                    for k in best_paths:
                        paths_file.write(f'{k}\n')
                    paths_file.write('\n\n')
        print(f'{lines} paths written to {file_name}')

############# Utils ##############
#
# This section should probably be moved somewhere else, like `utils`.
#

def create_list(tmp_list):
    """
    Create a list from user input via terminal.
    """
    while True:
        residue = input("\nInsert a residue, such as `ALA2` or `ala2`, or type `x` if completed:\n")
        if residue.lower() != 'x':
            tmp_list.append(residue.upper())
        else:
            break


def create_json(filename="./template.json"):
    """
    filename: (string) the file name to which write the json file


    The idea is to have a terminal interface to create the json file,
    if for some reason the user does not know how to write a json
    """
    if filename == "./template.json":
        tmp_dict = {
                    'source': ['MET1', 'PRO45'],
                    'target': ['LYS34', 'CYS98']
                    }
    else:
        print("Write terminal interface")
        tmp_dict = defaultdict(list)
        print("Initialising the source residues.")
        create_list(tmp_dict['source'])
        print("Initialising the target residues.")
        create_list(tmp_dict['target'])

    with open(filename, "w") as f:
        json.dump(tmp_dict, f)


def create_directory(folder="./output_analysis"):
    """
    Create the given directory and missing parent directories
    :param folder:
    :return:
    """
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    if os.path.exists(os.path.dirname(folder)):
        return folder
    else:
        raise RuntimeError(f"Could not create output folder {folder}")

def main():
    ########################## ARGUMENT PARSER ############################
    parser = argparse.ArgumentParser()

    d_helpstr = \
        ".dat file matrices (multiple: -d file.dat -d file2.dat ...)"
    parser.add_argument("-d", "--input-dat",
                        dest = "datfiles",
                        help = d_helpstr,
                        action = "append",
                        default = None)
    i_helpstr = \
        ".dat IIN file matrix"
    parser.add_argument("-i", "--input-IIN-dat",
                        dest = "iindatfile",
                        help = i_helpstr,
                        action = "store",
                        default = None)
    g_helpstr = \
        "topology file"
    parser.add_argument("-g", "--topology-file",
                        dest = "topol",
                        help = g_helpstr,
                        action = "store",
                        default = None)
    o_default = 'out_IIN.dat'
    o_helpstr = "Output .dat file matrix"
    parser.add_argument("-o", "--output-dat",
                        dest = "out_dat",
                        help = o_helpstr,
                        action = "store",
                        type = str,
                        default = o_default)
    p_default = 0.0
    p_helpstr = \
        "Filter input matrices according to this threshold (default: {:f})"
    parser.add_argument("-p", "--filter-threshold",
                        dest = "filter",
                        help = p_helpstr.format(p_default),
                        type = float,
                        default = p_default)
    s_helpstr = \
        "residue to calculate the sb for (-s RES1)"
    parser.add_argument("-s", "--sb_res",
                        dest = "sb_res",
                        help = s_helpstr,
                        action = "store",
                        default = None)
    t_helpstr = \
            "source and targer residues for sb (multiple: -t RES1 RES2)"
    parser.add_argument("-t", "--sb_path_res",
                        dest = "sb_path_res",
                        help = t_helpstr,
                        action = "store",
                        nargs = 2,
                        default = None)
    z_helpstr = \
        "json file containing source and target residues (-z file_source_target.json)"
    parser.add_argument("-z", "--shortest-path",
                        dest = "do_sh_path",
                        help = z_helpstr,
                        action = "store",
                        default = None)

    j_default = "./template.json"
    j_helpstr = \
        "creates a json-formatted file if you are a nabbo"
    parser.add_argument("-j", "--json",
                        dest = "do_json",
                        help = j_helpstr,
                        type = str,
                        nargs = '?',
                        const = j_default)
    flags = parser.parse_args()

    ########################### CHECK INPUTS ##############################
    if flags.do_json:
        print(f"Creating {flags.do_json} file")
        create_json(flags.do_json)

    if flags.datfiles:
        macro_iin = macroIIN_generator(matrices_list=flags.datfiles, p_crit=flags.filter, out_file=flags.out_dat)
    elif flags.iindatfile:
        macro_iin = np.loadtxt(flags.iindatfile)
    else:
        log.error("Input ddd file(s) must be provided.")
        exit(1)

    ############################# OUTPUT DAT ##############################

    if flags.do_sh_path:

#        source_res = list()
#        target_res = list()
#
#        source = True
#
#        with open(flags.do_sh_path) as res_file:
#            for line in res_file:
#                line = line.strip('\n').strip(' ')
#                if source:
#                    if 'target_res' in line:
#                        source = False
#                    elif line.strip() != '' and not line.startswith('#'):
#                        for res in line.split():
#                            source_res.append(res)
#                elif line.strip() != '' and not line.startswith('#'):
#                    for res in line.split():
#                        target_res.append(res)
        try:
            final_network = network_generator(network_matrix=macro_iin, topology_file=flags.topol)
        except TypeError:
            print('topology file must be provided with "-g" or "--topology-file"')
            exit(1)

        with open(flags.do_sh_path) as res_file:
            res_dict = json.load(res_file)

        try:
            source_res = res_dict['source']
            target_res = res_dict['target']
        except KeyError:
            print("The json file must have two keyword:")
            print("\t`source` and `target`.")
            print("Please check your json file or generate a new one.")

        print(f'source nodes:{source_res}')
        print(f'source nodes:{target_res}')

        all_shortest_paths(G = final_network,
                        source_res = source_res,
                        target_res = target_res,
                        threshold = flags.filter)

    if flags.sb_path_res or flags.sb_res:
        if flags.sb_path_res and flags.sb_res:
            try:
                final_network = network_generator(network_matrix=macro_iin, topology_file=flags.topol)
            except TypeError:
                print('topology file must be provided with "-g" or "--topology-file"')
                exit(1)
            selective_betweenness(G = final_network,
                                    source = flags.sb_path_res[0],
                                    target = flags.sb_path_res[1],
                                    sb_residue = flags.sb_res)
        else:
            print('both options -s and -t are required')





if __name__ == "__main__":
    main()



