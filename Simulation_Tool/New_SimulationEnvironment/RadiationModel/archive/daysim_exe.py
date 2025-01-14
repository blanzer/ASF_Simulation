import os,sys
import pandas as pd
import math
import multiprocessing
import shutil
import time
import json

from OCC import BRepGProp, GProp, TopoDS, BRep
from OCC.StlAPI import StlAPI_Reader
from OCCUtils import Topology

from pyliburo import gml3dmodel
from interface2py3d import pyptlist_frm_occface
import pyliburo
from pyliburo import py2radiance

from RadianceParameters import Library

def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list


def points_from_face(face):
    point_list = []
    pnt_coord = []
    wire_list = Topology.Topo(face).wires()
    for wire in wire_list:
        edges_list = Topology.Topo(wire).edges()
        for edge in edges_list:
            vertice_list = Topology.Topo(edge).vertices()
            for vertex in vertice_list:
                pnt_coord.append(
                    [BRep.BRep_Tool().Pnt(vertex).X(),
                     BRep.BRep_Tool().Pnt(vertex).Y(), BRep.BRep_Tool().Pnt(vertex).Z()])
    pnt_coord = make_unique(pnt_coord)
    for point in pnt_coord:
        point_list.append(point)
    return point_list


def add_rad_mat(aresults_path, abui, ageometry_table):
    file_path = os.path.join(aresults_path, abui + '\\rad\\' + abui +
                             "_material")
    file_name_rad = file_path + ".rad"
    file_name_txt = file_path + ".txt"
    os.rename(file_name_rad, file_name_rad.replace(".rad", ".txt"))
    with open(file_name_txt, 'a') as write_file:
        name_int = 0
        for geo in ageometry_table.index.values:
            mat_name = ageometry_table['mat_name'][geo]
            mat_value = ageometry_table['mat_value'][geo]
            string = "void plastic " + mat_name + " 0 0 5 " + str(mat_value) + " " + str(mat_value) + " " + str(mat_value) \
                     + " 0.0000 0.0000"
            write_file.writelines('\n' + string + '\n')
            name_int += 1
        write_file.close()
    os.rename(file_name_txt, file_name_rad.replace(".txt", ".rad"))


def percentage(task, now, total):
    percent = round((float(now)/float(total))*100, 0)
    division = 5
    number = int(round(percent/division, 0))

    bar = number * ">" + (100 / division - number) * "_"
    if now == total:
        print "\r", str(task), bar, percent, "%",
    else:
        print "\r", str(task),bar, percent, "%",


def geometry2radiance(arad, ageometry_table, project_path, project_folder, STLFolder):
    # parameters for the radiance
    
    ainput_path = STLFolder # set one general folder with all stl files
    #print 'STL', ainput_path
    
    # loop over all builings
    bcnt = 0
    for geo in ageometry_table.index.values:

        filepath = os.path.join(ainput_path, geo + ".stl")
        
        
        #print 'filepath', filepath # all .stl files with the name from the geometrytable list
        geo_solid = TopoDS.TopoDS_Solid()
        StlAPI_Reader().Read(geo_solid, str(filepath))


        face_list = pyliburo.py3dmodel.fetch.faces_frm_solid(geo_solid)

        bf_cnt = 0
        for face in face_list:
            bface_pts = pyptlist_frm_occface(face)
            srfname = "building_srf" + str(bcnt) + str(bf_cnt)

            srfmat = ageometry_table['mat_name'][geo]
            py2radiance.RadSurface(srfname, bface_pts, srfmat, arad)
            bf_cnt += 1
        bcnt += 1

"""
def calc_sensors(aresults_path, abui, ainput_path, axdim, aydim):

    print abui

    sen_df = []
    fps_df = []
    # import stl file
    filepath = os.path.join(ainput_path, abui + ".stl")
    geo_solid = TopoDS.TopoDS_Solid()
    StlAPI_Reader().Read(geo_solid, str(filepath))

    # calculate geometries properties
    props = GProp.GProp_GProps()
    BRepGProp.brepgprop_VolumeProperties(geo_solid, props)

    # reverse geometry if volume is negative
    if props.Mass() < 0:
        bui_vol = (-props.Mass())
        geo_solid.Reverse()
    else:
        bui_vol = (props.Mass())

    # get all faces from geometry
    face_list = pyliburo.py3dmodel.fetch.faces_frm_solid(geo_solid)

    fac_int = 0
    for face in face_list:


        normal = pyliburo.py3dmodel.calculate.face_normal(face)
        # calculate pts of each face
        fps = points_from_face(face)
        fps_df.append([val for sublist in fps for val in sublist])

        # calculate sensor points of each face
        sensor_srfs, sensor_pts, sensor_dirs = \
            gml3dmodel.generate_sensor_surfaces(face, axdim, aydim)
        fac_area = pyliburo.py3dmodel.calculate.face_area(face)
        # generate dataframe with building, face and sensor ID
        sen_int = 0

        for sen_dir in sensor_dirs:
            orientation = math.copysign(math.acos(normal[1]), normal[0]) * 180 / math.pi
            tilt = math.acos(normal[2]) * 180 / math.pi

            sen_df.append((fac_int, sen_int, fac_area, fac_area / len(sensor_dirs), sensor_pts[sen_int][0], sensor_pts[sen_int][1],
                 sensor_pts[sen_int][2], normal[0], normal[1], normal[2], orientation, tilt))
            sen_int += 1
        fac_int += 1

    sen_df = pd.DataFrame(sen_df, columns=['fac_int', 'sen_int', 'fac_area','sen_area', 'sen_x', 'sen_y',
                                       'sen_z', 'sen_dir_x', 'sen_dir_y', 'sen_dir_z', 'orientation', 'tilt'])
    sen_df.to_csv(os.path.join(aresults_path, abui + '_' + 'sen_df' + '.csv'), index=None, float_format="%.2f")

    fps_df = pd.DataFrame(fps_df, columns=['fp_0_0', 'fp_0_1', 'fp_0_2', 'fp_1_0', 'fp_1_1', 'fp_1_2', 'fp_2_0', 'fp_2_1', 'fp_2_2', ])
    fps_df.to_csv(os.path.join(aresults_path, abui + '_' + 'fps_df' + '.csv'), index=None, float_format="%.2f")
"""

def execute_daysim(name, aresults_path, arad, aweatherfile_path, rad_params, ageometry_table):
    
    
    sen_df = pd.read_csv(os.path.join(aresults_path, name + '_' + 'sen_df' + '.csv'))
    

    sen = sen_df[['sen_x', 'sen_y', 'sen_z']].values.tolist()
    sen_dir = sen_df[['sen_dir_x', 'sen_dir_y', 'sen_dir_z']].values.tolist()
    arad.set_sensor_points(sensor_normals=sen_dir, sensor_positions=sen)
    arad.create_sensor_input_file()

    # generate daysim result folders for all an_cores
    daysim_dir = os.path.join(aresults_path, name)
    arad.initialise_daysim(daysim_dir)
    # transform weather file
    arad.execute_epw2wea(aweatherfile_path)
    arad.execute_radfiles2daysim()

    add_rad_mat(aresults_path, name, ageometry_table)

    arad.write_radiance_parameters(rad_params['rad_ab'], rad_params['rad_ad'], rad_params['rad_as'],rad_params['rad_ar'],
                                   rad_params['rad_aa'], rad_params['rad_lr'],rad_params['rad_st'],rad_params['rad_sj'],
                                   rad_params['rad_lw'],rad_params['rad_dj'],rad_params['rad_ds'],rad_params['rad_dr'],
                                   rad_params['rad_dp'])


    #os.rename(os.path.join(arad.data_folder_path, abui + ".pts"), os.path.join(daysim_dir, 'pts', "sensor_points.pts"))

    arad.execute_gen_dc("w/m2")
    arad.execute_ds_illum()
    print name, 'done'


def execute_sum(results_path, bui):
    res = pd.read_csv(os.path.join(results_path, bui, 'res', bui+'.ill'), sep=' ', header=None)
    sums = res.ix[:, 4:].sum(axis=1)
    sums.columns = [bui]
    sums.to_csv(os.path.join(results_path, bui, 'res', bui+'.csv'), index=None)
    


def calc_radiation(geometry_table_name = None, sen_list=None, sensor_geometries_name=None, rad_params = None, paths = None):
    
  
    # =============================== parameters =============================== #
    paths['output'] = os.path.join(paths['project'], 'output')
    #input_path = os.path.join(project_path, 'input')
    
    with open(os.path.join(paths['input'],'weatherFile.json'),'w') as f:
            f.write(json.dumps(paths['Location']))
    # =============================== Preface =============================== #
      
            
    #rad = py2radiance.Rad(os.path.join(input_path, 'base.rad'), os.path.join(input_path, 'py2radiance_data'))
    rad = py2radiance.Rad(os.path.join(paths['Radiance'], 'base.rad'), os.path.join(paths['Radiance'], 'py2radiance_data'))

    # =============================== Import =============================== #
    geometry_table = pd.read_csv(os.path.join(paths['input'], geometry_table_name+".csv"), index_col='name')

    # =============================== Simulation =============================== #
    geometry2radiance(arad = rad, ageometry_table = geometry_table,  project_path = paths['main'], project_folder = paths['project'], STLFolder = paths['STL'])
    rad.create_rad_input_file()
    
    
    """
    # calculate sensor points
    if sen_list == None:
        #size of sensor points
        xdim = 5
        ydim = 5

        sensor_geometries = pd.read_csv(os.path.join(input_path, sensor_geometries_name + '.csv'), index_col='name')
        batch_names = sensor_geometries.index.values

        pool = multiprocessing.Pool()  # use all available cores, otherwise specify the number you want as an argument
        for bui in batch_names:
            pool.apply_async(calc_sensors, args=(results_path, bui, input_path, xdim, ydim,))
        pool.close()
        pool.join()
    """
    # load existing sensor points
    if sensor_geometries_name == None:
        batch_names = sen_list
        for sen in sen_list:
            sensor_file_path = os.path.join(paths['input'], sen + '.csv')
            sensor_file_path_output = os.path.join(paths['output'], sen + '_sen_df.csv')
            shutil.copyfile(sensor_file_path, sensor_file_path_output)
    ''''''
    
    # execute daysim
    processes = []
    for bui in batch_names:
        process = multiprocessing.Process(target=execute_daysim, args=(bui, paths['output'], rad, paths['Location'], rad_params, geometry_table,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()

    # calculate sums of each stl file
    pool = multiprocessing.Pool()
    for bui in batch_names:
        pool.apply_async(execute_sum, args=(paths['output'], bui,))
    pool.close()
    pool.join()




if __name__ == '__main__': 
    
   
#    XANGLES = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
#    YANGLES = [-45,-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45]
    XANGLES = [0]
    YANGLES = [0]
    
    ProjectSubFolder = 'Mat02'
    STLFolder = 'STL'
    geoLocation = 'Zuerich_Kloten_2013.epw'            
    RadianceValues = 'Default' #'MaxRad' #

    
    print '\nStart radiation calculation with daysim'
    print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
        
    tic = time.time()
    
    for x_angle in XANGLES:
        for y_angle in YANGLES:  
            print str(x_angle), str(y_angle)
                    
            geometry_table_name = 'background_geometries'
            #sensor_geometries_name = 'sensor_geometries'
            #sen_list = 'sen_dir'
            sen_list = ['ASF1_' + str(x_angle)+ '_' + str(y_angle),
                        'ASF2_' + str(x_angle)+ '_' + str(y_angle),
                        'ASF3_' + str(x_angle)+ '_' + str(y_angle),
                        'ASF4_' + str(x_angle)+ '_' + str(y_angle),
                        'Window'] #csv-file (sensor points, independent of stl-geometry files)
        
            
    
                        
           
            
            Project = 'ASF_' + str(x_angle) + '_' + str(y_angle)
            RadianceData = 'rad_data'
            
            paths = {}
            paths['Simulation_Environment'] =  os.path.abspath(os.path.dirname(sys.argv[0]))                       
            paths['main'] = os.path.join(paths['Simulation_Environment'], 'DaySimFolder')
            paths['weather_folder'] = os.path.join(paths['Simulation_Environment'], 'WeatherData')
            paths['project_SubFolder'] = os.path.join(paths['main'], ProjectSubFolder)
            paths['project'] = os.path.join(paths['project_SubFolder'], Project)
            paths['input'] = os.path.join(paths['project'], 'input')
            paths['pathFile'] = os.path.join(os.path.join(os.path.join(paths['project'], Project),'output\Window'), 'res\Window.csv')
            paths['Location'] = os.path.join(paths['weather_folder'], geoLocation)
            paths['STL'] = os.path.join(paths['main'], STLFolder)
            paths['Radiance'] = os.path.join(paths['main'], RadianceData)
            
            #3
            rad_params = Library(RadianceValues = RadianceValues)
           
            
            #option to chose    
            calc_radiation(geometry_table_name = geometry_table_name, sen_list = sen_list, rad_params = rad_params, paths = paths)
            
            #calc_radiation(input_path, project_path, geometry_table_name, weatherfile_path, sensor_geometries_name=sensor_geometries_name, rad_params = rad_params) #not tested
            
            print '\n' + Project + ' done'
            toc = time.time() - tic
            print 'time passed (min): ' + str(round(toc/60.,2))
