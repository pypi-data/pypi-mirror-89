"""
This is an objected-oriented file finder module.

It looks for files and folders in os directories, ftp location or in zip archives.
Search is based on regex.

Many options are available to stop or continue search when a file or folder is found.

"""
import logging
import os
import re
from ftplib import FTP
from datetime import datetime
from zipfile import ZipFile
from pathlib import Path


class Finder():
    """
    The Finder class offers convenient functions to search files and folders based on regex.
    """

    def __init__(self, settings=None):
        """
        builds the class according to the settings definition.
        Parameters
        ----------
        settings : object that may contain the following key and values

        - parent: gives the root directory into which files or folders should be searched. 
        If not set, the current folder (folder from which the script is launched) will be used

        - regex: regular expression used to check if a file or folder is part of the search. 
        It could be a single expression or a list of expressions
        Default value is '.*' : it looks for any file or folder. 
        If for example we want to list all files and folders of the parent folder, this default value may be used in association with depth=1

        - depth: depth of research. If set to 0, then files and folders are only searched in the parent folder. 
        If set to n (n as an integer), then search goes up to the n-th subdirectory. 
        Default value is -1, which means that search doesn't stop while there is no more subfolder.

        - stopWhenFound: as soon as a file or folder complies with the regex, the search is topped and the found file or folder is returned 
        (in an array) to satisfy the more generic research. Default value is True.

        - goIntoFoundFolder: When False, if a folder is searched and found, does not look inside for subfolders that comply with regex. 
        This is different of stopWhenFound: it may find multiple folders but does not look into a found folder. Default value is False.

        - avoidFolders: array of folder names to exclude in the search. Does not either return these folders or look into. 
        Default value is empty.

        - caseSensitive: if true, the regex is case sensitive. Default value is True.

        - ftpConnection: ftp connection to be used when looking in a ftp location. 
        This connection is returned when calling ftplib FTP(host, user, pwd)

        """
        self.parent = os.getcwd()
        self.regex = ['.*']
        self.depth = -1
        self.stopWhenFound = True
        self.goIntoFoundFolder = False
        self.avoidFolders = []
        self.caseSensitive = True
        self.ftpConnection = None
        self._setProperties(settings)
        self.parent = str(Path(self.parent).resolve()
                          ) if self.parent != '/' else self.parent
        self.initialDepth = 0

    def getRootFile(self, parent, regex):
        self.parent = parent
        self.depth = 0
        self.caseSensitive = False
        self.regex = regex
        files = self.findFiles()
        if files is None:
            return None
        return files[0]

    def findFolders(self):
        """
        find folders in the os directory according to the settings defined when building the Finder object
        """
        self.initialDepth = self.parent.count(os.path.sep)
        folders, _ = self._findAllFolders(self._walkFile)
        return folders

    def matchFolders(self):
        """
        find folders in os directory according to the settings defined when building the Finder object; 
        If every regex returns a result, then match is true
        """
        self.initialDepth = self.parent.count(os.path.sep)
        logging.debug('looking for {} in {}'.format(self.regex, self.parent))
        founds, missed = self._findAllFolders(self._walkFile)
        return (len(missed) == 0, founds, missed)

    def findFoldersInFtp(self):
        """
        find folders in the ftp location according to the settings defined when building the Finder object
        """
        self.initialDepth = self.parent.count('/')
        folders, _ = self._findAllFolders(self._walkFTP, sep='/')
        return folders

    def findFiles(self):
        """
        find files in os directory according to the settings defined when building the Finder object
        """
        self.initialDepth = self.parent.count(os.path.sep)
        logging.debug('looking for {} in {}'.format(self.regex, self.parent))
        files, _ = self._findAllFiles(self._walkFile)
        return files

    def matchFiles(self):
        """
        find files in os directory according to the settings defined when building the Finder object; 
        If every regex returns a result, then match is true
        """
        self.initialDepth = self.parent.count(os.path.sep)
        logging.debug('looking for {} in {}'.format(self.regex, self.parent))
        founds = []
        regex = []
        match = True
        all_regex = self.regex.copy()
        for reg in all_regex:
            self.regex = [reg]
            files, missed = self._findAllFiles(self._walkFile)
            match = match and not not files
            founds += files
            if missed:
                regex += missed
        
        return (match, founds, regex)

    def findFilesInFtp(self):
        """
        find files in ftp location according to the settings defined when building the Finder object
        """
        self.initialDepth = self.parent.count('/')
        files, _ = self._findAllFiles(self._walkFTP, sep='/')
        return files

    def findFilesInZip(self):
        """
        find files in a zip archive according to the settings defined when building the Finder object.
        In this case the "parent" setting should be the zip path
        """
        files, _ = self._findAllFiles(self._walkZip, sep='/')
        return files

    def _setProperties(self, settings: dict):
        if not settings:
            return
        for key in settings:
            if hasattr(self, key):
                setattr(self, key, settings[key])
        if type(self.regex) is not list:
            self.regex = [self.regex]

    def _findAllFiles(self, callback, sep=os.path.sep):
        found_files = []
        missed = []
        for regex in self.regex:
            files = self._findFiles(callback, sep, regex)
            if not files:
                missed.append(regex)
            found_files += files
        return found_files, missed

    def _findFiles(self, callback, sep, regex):
        foundFiles = []
        flags = 0 if self.caseSensitive else re.IGNORECASE
        compiled = re.compile(regex, flags)
        for dirpath, subdirs, files in callback(self.parent):
            logging.debug('scanning {}'.format(dirpath))
            foundFiles += [dirpath+sep+filename
                           for filename in files if compiled.search(filename)]
            if self.stopWhenFound and foundFiles:
                return [foundFiles[0]]
            for avoidFolder in self.avoidFolders:
                if avoidFolder in subdirs:
                    subdirs.remove(avoidFolder)
        return foundFiles

    def _findAllFolders(self, callback, sep=os.path.sep):
        found_folders = []
        missed = []
        for regex in self.regex:
            logging.debug('regex=%s', regex)
            folders = self._findFolders(callback, sep, regex)
            logging.debug('folders=%s', folders)
            if not folders:
                logging.debug('folders=%s', folders)
                missed.append(regex)
            found_folders += folders
        return found_folders, missed

    def _findFolders(self, callback, sep, regex):
        folders = []
        flags = 0 if self.caseSensitive else re.IGNORECASE
        try:
            compiled = re.compile(regex, flags)
        except:
            logging.error('wrong regex search')
            return
        for dirpath, subdirs, _ in callback(self.parent):
            logging.debug('processing folder {}'.format(dirpath))
            founds = [subdir for subdir in subdirs if compiled.search(subdir)]
            if founds and self.stopWhenFound:
                return founds
            folders += [dirpath+sep+subdir for subdir in founds]
            for subdir in founds:
                if not self.goIntoFoundFolder:
                    subdirs.remove(subdir)
            for avoidFolder in self.avoidFolders:
                if avoidFolder in subdirs:
                    subdirs.remove(avoidFolder)
        logging.debug('{} folders found'.format(len(folders)))
        return folders

    def _walkFile(self, path):
        for root, dirs, files in os.walk(path):
            num_sep_this = root.count(os.path.sep)
            yield root, dirs, files
            if self.initialDepth + self.depth <= num_sep_this and self.depth > -1:
                del dirs[:]

    def _walkZip(self, path):
        """
        Walk through Zip archive
        """
        zipFile = ZipFile(path, 'r')
        itemsInZip = zipFile.namelist()
        dirs = []
        nondirs = []
        for item in itemsInZip:
            groups = item.split('/')
            num_sep_this = len(groups) - 2
            if self.depth < num_sep_this and self.depth > -1:
                continue
            if item.endswith('/'):
                dirs.append(groups[-2])
            else:
                nondirs.append(groups[-1])
        yield path, dirs, nondirs

    def _listdirFTP(self, _path):
        dirs = []
        nondirs = []
        file_list = self._getFtpFileInfo(_path)
        for info in file_list:
            ls_type, name = info[0], info[-1]
            if re.match(r'^\.+$', name):
                continue
            if ls_type.startswith('d'):
                dirs.append(name)
            else:
                nondirs.append(name)
        return dirs, nondirs

    def _getFtpFileInfo(self, _path):
        """
        return files and directory names within a path (directory)
        """
        file_list = []
        try:
            self.ftpConnection.cwd(_path)
        except Exception as exp:
            logging.error(exp.__str__(), _path)
            return []
        else:
            self.ftpConnection.retrlines(
                'LIST', lambda x: file_list.append(x.split()))
        return file_list

    def _walkFTP(self, path):
        """
        Walk through FTP server's directory tree, based on a BFS algorithm.
        """
        dirs, nondirs = self._listdirFTP(path)
        num_sep_this = path.count('/')
        yield path, dirs, nondirs
        if self.initialDepth + self.depth <= num_sep_this and self.depth > -1:
            del dirs[:]
        for name in dirs:
            yield from self._walkFTP(path+'/'+name)
            self.ftpConnection.cwd('.')
