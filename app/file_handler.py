#!/usr/bin/python
#Copyright (c) by linhtx
# -*- coding: utf-8 -*-
import os
import shutil

class FileHandler:
    
    def copyFile(self, source, destination, fileName):
        source = os.path.join(source)
        destination = os.path.join(destination)
        if not os.path.exists(destination):
            os.makedirs(os.path.join(destination))
        shutil.copyfile(source, os.path.join(destination, fileName))
    
    def writeFile(self, filePath, data):
        with open(filePath, 'w') as file:
            file.write(data)


    def replaceAndWriteFile(self, destination, dataObject):
        with open(destination, 'r') as file:
            data = file.read()
            for key in dataObject:
                data = data.replace(key, dataObject[key])

        self.writeFile(destination, data)

    def handleFile(self, source, destination, fileName, dataObject):
        self.copyFile(source, destination, fileName)
        if (len(dataObject) > 0):
            self.replaceAndWriteFile(os.path.join(destination, fileName), dataObject)
    