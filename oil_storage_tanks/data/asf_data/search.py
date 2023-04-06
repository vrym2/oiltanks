"""Functions relating to search"""
import os
import numpy as np
import logging
from datetime import datetime
from typing import Dict

try:
    import asf_search as asf
    from oil_storage_tanks.utils import stitch_strings
    from oil_storage_tanks.data import bounding_box as bbox
    from oil_storage_tanks.data import oil_terminals
except ImportError as e:
    logging.debug(f"Import error: {e}")


class search_earthdata():
    """Refine Search results from ASF EARTH DATA"""
    def __init__(
            self,
            start_date:str = "2023-03-10",
            end_date:str = "2023-03-18",
            location_name:str = "flotta",                      
            log=None) -> None:
        """Getting the meta data of the scene
        
        Args:
            start_date: Start date of the search
            end_date: End date of the search
            location_name: Location name of the oil terminal
            log: Custom logger function        
        """       
        self.start_date = start_date
        self.end_date = end_date
        self.location_name = location_name
        self.log = log

    def region_coords(
            self,
            oil_terminal_path: str = None)-> None:
        """Getting the coordinates"""
        if not os.path.exists(oil_terminal_path):
            self.log.error(f"{oil_terminal_path} does not exist!")
            self.log.debug("Add correct path to the oil terminal file")
        else:
            oil_terminal_data = oil_terminals(
                terminal_file_path = oil_terminal_path)
            try:
                self.center_coords_lat = oil_terminal_data[self.location_name][0]
                self.center_coords_lon = oil_terminal_data[self.location_name][1]
            except IndexError:
                self.log.error(f"{self.location_name} is not in the file")
                self.log.debug("Choose an appropriate location name!")

    def metadata(self):
        # Getting the WKT from center coordinates
        self.log.info(f"Looking data for the coords:{self.center_coords_lat},{self.center_coords_lon}")
        self.wkt_aoi = bbox(
            center_lat = self.center_coords_lat,
            center_lon = self.center_coords_lon)

        # Date objects
        self.log.info(f"Searching data for the dates between {self.start_date} : {self.end_date}")
        self.start = datetime.strptime(self.start_date, "%Y-%m-%d")
        self.end = datetime.strptime(self.end_date, "%Y-%m-%d")

        # Getting the results of the search
        self.results = asf.search(
            platform= asf.PLATFORM.SENTINEL1A,
            processingLevel=[asf.PRODUCT_TYPE.SLC],
            start = self.start,
            end = self.end,
            intersectsWith = self.wkt_aoi
            )
        
        # Sanity check
        try:
            total_results = len(self.results)
            assert total_results > 0
            self.log.info(f'Total Images Found: {len(self.results)}')
            ### Save Metadata to a Dictionary
            self.metadata = self.results.geojson()
            return self.metadata 
                   
        except AssertionError:    
            self.log.debug("No images are found for the given criteria!")
            return None
    
    def save_search(
            self,
            csv_file_save_path: str):
        """Fucntion to save the search results"""
        # Definig the filename and the path
        start_date = self.start_date.replace('-', '')
        end_date = self.end_date.replace('-', '')
        filename = ["s1", self.location_name, start_date, end_date]
        filename = stitch_strings(filename, "_")
        self.csv_folderpath = os.path.join(csv_file_save_path, self.location_name)
        self.csv_filepath = os.path.join(self.csv_folderpath, filename + ".csv")

        # Writing the file
        if not os.path.exists(self.csv_folderpath):
            self.log.info(f"Creating the folder {self.location_name}")
            os.makedirs(self.csv_folderpath)
        else:
            self.log.debug(f"The folder '{self.location_name}' exists!")

        if not os.path.isfile(self.csv_filepath):
            with open(self.csv_filepath, "w") as f:
                f.writelines(self.results.csv())
                f.close()
                self.log.info(f"The file is saved to: {self.csv_filepath}")
        else:
            self.log.debug(f"The file already exists: {self.csv_filepath}")
        
        return self.csv_filepath