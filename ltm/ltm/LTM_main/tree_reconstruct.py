import calculate_paralinear_dist as cpd
import recursive_grouping as rg
import chow_liu_grouping as clg
import timeit


class Recon_Method:
    RECURSIVE_GROUPING = 1
    CHOW_LIU_GROUPING = 2
  
# Settings for reconstructing a tree from data      
class Recon_Settings:
    def __init__(self, method, tau = None, epsilon = None):
        self.method = method
        self.tau = tau
        self.epsilon = epsilon
        
def reconstruct(recon_settings, position_data, cell_data, alphabet):
    
    start = timeit.default_timer()
        
    # Reconstruct the tree
    if (recon_settings.method == Recon_Method.RECURSIVE_GROUPING):
        observed_vertices = sorted(cell_data.keys())
        D = get_distance_matrix(cell_data, observed_vertices, alphabet)
        
        # For comparison with matlab code
#         mat_D = convert_distmat_to_matlab(D, observed_vertices)
#         f = open("matlab_D.txt",'w')
#         f.write(mat_D)
#         f.close()
#         
#         mat_celldat = convert_celldat_to_matlab(cell_data)
#         f = open("matlab_celldat.txt",'w')
#         f.write(mat_celldat)
#         f.close()
        
        result_tree = rg.recursive_grouping(D,observed_vertices,observed_vertices[-1],observed_vertices[-1] + 1,recon_settings.tau,recon_settings.epsilon)
  
    elif (recon_settings.method == Recon_Method.CHOW_LIU_GROUPING):
        observed_vertices = sorted(cell_data.keys())
        D = get_distance_matrix(cell_data, observed_vertices, alphabet)
        result_tree = clg.chow_liu_grouping(D,position_data.values(),observed_vertices,recon_settings.tau,recon_settings.epsilon)
        
    else:
        raise Exception("Invalid Reconstruct Method")
    
    stop = timeit.default_timer()
    run_time = stop - start
    
    return (result_tree, run_time)


def get_distance_matrix(cell_data, vertices, alphabet):
    D = dict()
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            distance = cpd.calculate_distance(cell_data[vertices[i]], cell_data[vertices[j]], alphabet)
            D[(vertices[i],vertices[j])] = distance
            D[(vertices[j],vertices[i])] = distance
    return D

def convert_distmat_to_matlab(distance_matrix, vertices):
    out_string = "["
    first_row = True
    for i in vertices:
        if not first_row:
            out_string += "; "
        for j in vertices:
            if (i,j) not in distance_matrix:
                out_string += str(0) + " "
            else:
                out_string += str(distance_matrix[(i,j)]) + " "
        first_row = False
    out_string += "]"
    return out_string

def convert_celldat_to_matlab(cell_data):
    out_string = "["
    first_row = True
    for cell_string in cell_data.values():
        if not first_row:
            out_string += "; "
        for c in cell_string:
            if c == '0':
                out_string += "1 "
            else:
                out_string += "2 "
        first_row = False
    out_string += "]"
    return out_string
            







    