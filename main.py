import random
def to_datadivr(G, name, pos, nodecolor, annotation, cluster, linkcolor):
    """
    "name" = string i.e. title of the graph

    "pos" = dict, key = node id, value = coordinates (x,y,z) as tuple

    "nodecolor" = dict, key = node id, value = color (hex = string or rgba = tuple(r,g,b,a) between 0-255)

    "annotation" = list of strings, separated with a ";" E.g. it can store info on a person (i.e. node in social network) "name; age; height; ..."

    "cluster" = dict, key = node id, value = clustername as string

    "linkcolor" = dict, key = link id as tuple (start,end), value = color (hex = string or rgba = tuple(r,g,b,a) between 0-255)
    """
    # --------------------------
    # Generate VR GRAPH 
    # --------------------------
    GVR = nx.Graph()
    GVR.graph['name'] = name

    # --------------------------------------
    # LOOKUP FOR NODE NAMES INTO IDs and vv
    # --------------------------------------

    d_idx_node = {}
    d_node_idx = {}
    for i, node in enumerate(sorted(G.nodes())):
        d_idx_node[i] = node
        d_node_idx[node] = i
    
    GVR.add_nodes_from(d_idx_node.keys())

    # d_edge_color = {}
    for edge in G.edges()(data=True):
        GVR.add_edge(d_node_idx[edge[0]],d_node_idx[edge[1]])
    # --------------------------
    # POS 
    # --------------------------
    # pos = nx.spring_layout(GVR, dim = 3)
    
    coords = {d_node_idx[i]:v.tolist() for i,v in pos.items()}
    nx.set_node_attributes(GVR, coords, name="pos")

    # # --------------------------
    # # CLUSTER 
    # # --------------------------

    # assign c clusters randomly
    c = 1
    assigned_groups = []
    for g in sorted(GVR.nodes()):
        n = random.randint(0,c)
        assigned_groups.append(n)
    dict_for_cluster = dict(zip(d_idx_node.keys(), assigned_groups))
    nx.set_node_attributes(GVR, dict_for_cluster, name="cluster")

    # --------------------------
    # NODE COLOR  
    # --------------------------

    # assign a colors to node
    # single color
    col = '#f8b100'
    d_node_colors={}
    for nodeid in GVR.nodes():
        d_node_colors[nodeid] = col

    nx.set_node_attributes(GVR, d_node_colors, name="nodecolor")

    # --------------------------
    # NODE ANNOTATION
    # --------------------------

    l_annotations = ['Node: '+str(d_idx_node[nodeid]) for nodeid in GVR.nodes()] # j -> nodeid
    d_annotations = dict(zip(GVR.nodes(), l_annotations))
    nx.set_node_attributes(GVR, d_annotations, name="annotation")

    # --------------------------
    # LINK COLOR
    # --------------------------

    list_of_colors = sns.color_palette("Set2", n_colors=4).as_hex()

    # here you can also use a dict instead of just one color value
    d_edge_color = {}
    single_edge_col = linkcolor
    for a,b in GVR.edges():
        # d_edge_color[(a,b)] = random.choice(list_of_colors)
        
        try:
            d_edge_color[(a,b)] = linkcolor[(d_idx_node[a],d_idx_node[b])]

        except KeyError:
            d_edge_color[(a,b)] = linkcolor[(d_idx_node[b], d_idx_node[a])]
    
    nx.set_edge_attributes(GVR, d_edge_color, name="linkcolor")
    
    return GVR
    
GVR = to_datadivr(G_corr, "Feature_Correlations_normalized", pos, nodecolor, annotation, cluster, linkcolor)
G_json = json.dumps(nx.node_link_data(GVR))

with open(GVR.name+".json", "w") as outfile:
    outfile.write(G_json)
