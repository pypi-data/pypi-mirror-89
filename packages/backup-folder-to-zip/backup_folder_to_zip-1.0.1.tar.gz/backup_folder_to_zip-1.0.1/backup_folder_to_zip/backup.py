#! python3

import zipfile, os, sys, errno

class Backup (): 
    """ 
    Main class. Copies an entire folder and its contains into a zip file whose 
    filename increments.
    """

    def __init__ (self, folderToZip, folderDestination): 
        """ 
        Constructor of the class. 
        Get the folder to backup in zip file, and the folder estinarion of the zip file
        """

        self.folderToZip = folderToZip
        self.folderDestination = folderDestination        

        self.__verify_paths()

        self.zipFilename = self.__get_name_zip_file()

        self.__backup_folder()

        
    def __verify_paths (self):
        """
        Verify is the from and the to path exist in the pc
        """ 

        # Verify the paths
        if not os.path.exists (self.folderToZip): 
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.folderToZip)
        
        if not os.path.exists (self.folderDestination): 
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.folderDestination)


    def __get_name_zip_file (self): 
        """
        Generate and return the name of the zip file. 
        If file already exist, increase the number 
        """

        number = 1
        while True: 
            os.chdir (self.folderDestination)
            zipFilename = os.path.basename(self.folderToZip) + '_' + str(number) + '.zip'
            if not os.path.exists(zipFilename):
                break
            number += 1
        
        return zipFilename


    def __backup_folder (self): 
        """ 
        Backup the folder
        """

        print ('Creating "{}" file...'.format (self.zipFilename))

        # Make and open file
        os.chdir (self.folderDestination)
        backupZip = zipfile.ZipFile(self.zipFilename, 'w')


        #Walk the entire folder tree and compress the files in each folder.
        os.chdir (self.folderToZip)
        for foldername, subfolders, filesnames in os.walk('.'):

            # Add the current folder to the zip file
            backupZip.write(foldername)

            # Add all files in this folder, to the Zip file
            for filename in filesnames: 
                newBase = os.path.basename(self.folderToZip) + '_' 
                
                #Checks the starts of the file
                if filename.startswith(newBase) and filename.endswith('.zip'):
                    continue # Dont backup the backup zip files

                backupZip.write(os.path.join(foldername, filename))

        backupZip.close()
        print ('Done.')

