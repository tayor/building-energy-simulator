from math import sqrt
def surface_util(surface,x1=0,y1=0,z1=0,x2=0,y2=0,z2=0,x3=0,y3=0,z3=0,x4=0,y4=0,z4=0):
    surface.Vertex_1_Xcoordinate=x1
    surface.Vertex_1_Ycoordinate=y1
    surface.Vertex_1_Zcoordinate=z1
    surface.Vertex_2_Xcoordinate=x2
    surface.Vertex_2_Ycoordinate=y2
    surface.Vertex_2_Zcoordinate=z2
    surface.Vertex_3_Xcoordinate=x3
    surface.Vertex_3_Ycoordinate=y3
    surface.Vertex_3_Zcoordinate=z3
    surface.Vertex_4_Xcoordinate=x4
    surface.Vertex_4_Ycoordinate=y4
    surface.Vertex_4_Zcoordinate=z4
    return surface

def surfaces(batiment, x=10, y=20, z=3.5):
    surfaces=batiment.idfobjects["BUILDINGSURFACE:DETAILED"]
    surfaces[0]=surface_util(surfaces[0], x1=x, y3=y, x4=x, y4=y)
    surfaces[1]=surface_util(surfaces[1], z1=z, x2=x, z2=z, x3=x, y3=y, z3=z, y4=y, z4=z)
    surfaces[2]=surface_util(surfaces[2], x1=x, x2=x, y2=y, x3=x, y3=y, z3=z, x4=x, z4=z)
    surfaces[3]=surface_util(surfaces[3], x1=x, y1=y, y2=y, y3=y, z3=z, x4=x, y4=y, z4=z)
    surfaces[4]=surface_util(surfaces[4],y1=y, z3=z,y4=y, z4=z)
    surfaces[5]=surface_util(surfaces[5],x2=x, x3=x, z3=z, z4=z)
    return batiment

def window_util(s, w, p):
    w.Vertex_1_Xcoordinate = s.Vertex_1_Xcoordinate + sqrt(p)*(s.Vertex_4_Xcoordinate+s.Vertex_2_Xcoordinate- 2*s.Vertex_1_Xcoordinate)/2
    w.Vertex_1_Ycoordinate = s.Vertex_1_Ycoordinate + sqrt(p)*(s.Vertex_4_Ycoordinate+s.Vertex_2_Ycoordinate- 2*s.Vertex_1_Ycoordinate)/2
    w.Vertex_1_Zcoordinate= s.Vertex_1_Zcoordinate + sqrt(p)*(s.Vertex_4_Zcoordinate+s.Vertex_2_Zcoordinate- 2*s.Vertex_1_Zcoordinate)/2
    w.Vertex_2_Xcoordinate= s.Vertex_2_Xcoordinate + sqrt(p)*(s.Vertex_1_Xcoordinate+s.Vertex_3_Xcoordinate- 2*s.Vertex_2_Xcoordinate)/2
    w.Vertex_2_Ycoordinate= s.Vertex_2_Ycoordinate + sqrt(p)*(s.Vertex_1_Ycoordinate+s.Vertex_3_Ycoordinate- 2*s.Vertex_2_Ycoordinate)/2
    w.Vertex_2_Zcoordinate= s.Vertex_2_Zcoordinate + sqrt(p)*(s.Vertex_1_Zcoordinate+s.Vertex_3_Zcoordinate- 2*s.Vertex_2_Zcoordinate)/2
    w.Vertex_3_Xcoordinate= s.Vertex_3_Xcoordinate + sqrt(p)*(s.Vertex_2_Xcoordinate+s.Vertex_4_Xcoordinate- 2*s.Vertex_3_Xcoordinate)/2
    w.Vertex_3_Ycoordinate= s.Vertex_3_Ycoordinate + sqrt(p)*(s.Vertex_2_Ycoordinate+s.Vertex_4_Ycoordinate- 2*s.Vertex_3_Ycoordinate)/2
    w.Vertex_3_Zcoordinate= s.Vertex_3_Zcoordinate + sqrt(p)*(s.Vertex_2_Zcoordinate+s.Vertex_4_Zcoordinate- 2*s.Vertex_3_Zcoordinate)/2
    w.Vertex_4_Xcoordinate= s.Vertex_4_Xcoordinate + sqrt(p)*(s.Vertex_3_Xcoordinate+s.Vertex_1_Xcoordinate- 2*s.Vertex_4_Xcoordinate)/2
    w.Vertex_4_Ycoordinate= s.Vertex_4_Ycoordinate + sqrt(p)*(s.Vertex_3_Ycoordinate+s.Vertex_1_Ycoordinate- 2*s.Vertex_4_Ycoordinate)/2
    w.Vertex_4_Zcoordinate= s.Vertex_4_Zcoordinate + sqrt(p)*(s.Vertex_3_Zcoordinate+s.Vertex_1_Zcoordinate- 2*s.Vertex_4_Zcoordinate)/2
    return w

def windows(batiment, p=0.10):
    surfaces=batiment.idfobjects["BUILDINGSURFACE:DETAILED"]
    windows=batiment.idfobjects["FENESTRATIONSURFACE:DETAILED"]
    for i in range(2,6):
        windows[i-2]=window_util(surfaces[i],windows[i-2], p)
    return batiment
