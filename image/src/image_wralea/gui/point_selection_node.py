def point_selection(im,points,new_points):
    from copy import deepcopy
    if new_points is None: 
        return deepcopy(im),deepcopy(points)
    else : 
        return deepcopy(im),deepcopy(new_points)
