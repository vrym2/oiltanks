"""Downloading data from Copernicus Data Hub"""
import os
from oil_storage_tanks.data import auth_credentials

class download_data(auth_credentials):
    """Function to download single scene"""
    def __init__(
            self, 
            data_service: str = None, 
            path_to_cred_file: str = None,
            username:str = None,
            password:str = None,            
            log=None) -> None:
        super().__init__(
            data_service, path_to_cred_file,
            username, password, log)
        self.api = super().scihub_auth()
    
    def download_sensat(
            self,
            uuid:str = None,
            title:str = None,
            download_path: str = None)-> None:
        """Downloading a single product
        
        Args:
            title: title of the file
            uuid: Identifier of the a file
            download_path: Download path folder
        """
        file_ext = title + '.zip'
        filepath = os.path.join(download_path, file_ext)
        if not os.path.exists(filepath):
            self.log.info(f"Commencing {title} download")
            self.api.download(uuid, download_path)
            return filepath
        else:
            self.log.debug("File already exists!")
            return filepath
