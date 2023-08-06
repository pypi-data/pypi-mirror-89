#! python

import os, shutil, sys, errno

class Copy (): 
    """ 
    Copy a specific file extension in the tree directory 
    """

    def __init__ (self, from_path, to_path, extention): 
        """
        Constructor of class. Get paths and extension. Generate file list
        """

        self.from_path = from_path
        self.to_path = to_path
        self.extention = extention
        self.files = [] 

        self.__verify_paths ()

        self.__find_files()
        self.__copy_files()

    def __verify_paths (self):
        """
        Verify is the from and the to path exist in the pc
        """ 

        # Verify the paths
        if not os.path.exists (self.from_path): 
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.from_path)
        
        if not os.path.exists (self.to_path): 
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.to_path)

    def __find_files (self): 
        """
        Search all files inside the from folder, and save the 
        full path of the files that match the searched extension.
        """

        # Check correct extension
        if not self.extention.startswith('.'): 
            self.extention = '.' + self.extention #Add a dot

        absPath = os.path.abspath(self.from_path)

        # walk inside the origin tree
        for folder_name, subfolder_name, file_names in os.walk(absPath): 
            
            # if the file has the correct extension, save complite path
            for file in file_names: 
                if file.endswith(self.extention):
                    self.files.append(os.path.join(folder_name, file))
    
    def __copy_files (self):
        """ 
        Loop inside a list of files and copy to destiny
        """

        # Check if exist files in file list
        if self.files: 

            absPath = os.path.abspath(self.to_path)

            for file in self.files: 
                print ('Copying "{}" to "{}" ...'.format (file, absPath))
                shutil.copy(file, absPath)
        else: 
            print ("No files found in from folder")
