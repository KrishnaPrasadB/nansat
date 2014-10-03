#-------------------------------------------------------------------------------
# Name:         test_nansat_archive.py
# Purpose:      To test nansat
#
# Author:       Morten Wergeland Hansen, Asuka Yamakawa
# Modified: Morten Wergeland Hansen
#
# Created:  18.06.2014
# Last modified:08.07.2014 11:03
# Copyright:    (c) NERSC
# License:
#-------------------------------------------------------------------------------
import os, warnings, time


class TestData(object):
    ''' Download test data and keep info about each file '''
    mapperData = None

    def __init__(self):
        ''' Set directory to store test data

        If MAPPER_TEST_DATA_DIR is in the environment its value will be used
        This is convenient for testing localy and sharing downloaded
        data among several users on the server
        '''
        self.testDataDir = os.getenv('MAPPER_TEST_DATA_DIR')
        if self.testDataDir is None:
            self.testDataDir = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'test_data')

    def download_all_test_data(self):
        ''' Download test data for each mapper '''
        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/asar/ASA_WSM_1PNPDE20120327_205532_000002143113_00100_52700_6903.N1',
                'asar')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/aster_l1a/AST_L1A_00306192003124632_20120731044546_8073.hdf',
                'aster_l1a')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/cosmoskymed/CSKS4_SCS_B_PP_11_CO_LA_FF_20111215040251_20111215040257.h5',
                'cosmoskymed')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/hirlam/DNMI-NEurope.grb',
                'hirlam')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/landsat/LC81750072013176LGN00.tar.gz',
                'landsat')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/meris/MER_FRS_1PNUPA20100916_105248_000001012093_00037_44680_8756.N1',
                'meris_l1')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/modis_l1/MOD021KM.A2010105.2120.005.2010106075131.hdf',
                'modis_l1')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/ncep/gfs.t00z.master.grbf00',
                'ncep')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/radarsat2/RS2_20140716_061819_0076_SCWA_HHHV_SGF_336560_2501_9900957.zip',
                'radarsat2')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/generic/mapperTest_generic.tif',
                'generic')

        self.download_test_file(
                'ftp://ftp.nersc.no/pub/python_test_data/obpg_l2/A2014275111000.L2_LAC.NorthNorwegianSeas.hdf',
                'obpg_l2')

    def download_test_file(self, inputURL, mapperName):
        ''' Download one file for one mapper

        For the given URL and mapper name
        Create local dir with name ./test_data/mapper_name/mapper_file.ext'
        If the downloaded file does not already exist:
            download the file into the dir
        Keep the filepath in self.mapper_data[mapper_name]

        Parameters:
        -----------
            inputUrl : str
                valid URL with the test file to download
            mapperName : str
                name of the mapper for which the data is downloaded

        ModifIes:
        ---------
            self.mapper_data : dict
                adds new <mapper_name> : [<testFileName>]
                or appends <testFileName> to the existing key

        '''
        fName = os.path.basename(inputURL)
        mapperDir = os.path.split(os.path.split(inputURL)[0])[1]
        mapperDataDir = os.path.join(self.testDataDir, mapperDir)
        mapperFName = os.path.join(mapperDataDir, fName)

        if not os.path.exists(mapperDataDir):
            os.makedirs(mapperDataDir)

        if not os.path.exists(mapperFName):
            print "Downloading %s " % mapperFName
            t0 = time.time()
            os.system('curl -so ' + mapperFName + ' ' + inputURL )
            print time.time() - t0

        if not os.path.isfile(mapperFName):
            warnings.warn( """
                    Could not access %s on ftp-site with test data - contact
                    morten.stette@nersc.no to get the ftp-server at NERSC restarted"""
                    % mapperFName)
        else:
            if self.mapperData is None:
                self.mapperData = {}
            if mapperName in self.mapperData:
                self.mapperData[mapperName].append(mapperFName)
            else:
                self.mapperData[mapperName] = [mapperFName]
