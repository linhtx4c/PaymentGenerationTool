#!/usr/bin/python
#Copyright (c) by linhtx
# -*- coding: utf-8 -*-
import os
import shutil
import re
from app.file_handler import FileHandler

class Module:

    def __init__(self, vendorName, moduleName, componentName):
        self.vendorName = vendorName
        self.componentName = componentName
        self.moduleName = moduleName
        self.fileHandler = FileHandler()
        self.sourcePath = 'source/'
        self.composerJsonFile = 'composer.json'
        self.registrationFile = 'registration.php'
        self.moduleFile = 'module.xml'
        self.etcPathFolder = 'etc'
        self.generateModule()
    
    def generateModule(self):
        if (self.vendorName != '' and self.moduleName != '' and self.componentName):
            if os.path.exists(self.vendorName):
                shutil.rmtree(self.vendorName)
            os.makedirs(os.path.join(self.vendorName, self.moduleName))
            self.handleComposerJsonFile()
            self.handleRegistrationFile()
            self.handleModuleFile()
        else:
            print('Module Name is not valid')


    # handle composer.json file
    def handleComposerJsonFile(self):
        destination = os.path.join(self.vendorName, self.moduleName)
        vendorLowerName = re.sub(r"(\w)([A-Z])", r"\1-\2", self.vendorName).lower()
        moduleLowerName = re.sub(r"(\w)([A-Z])", r"\1-\2", self.moduleName).lower()        
        data = {
            'VendorName': self.vendorName,
            'ModuleName': self.moduleName,
            'vendor-name': vendorLowerName,
            'module-name': moduleLowerName
        }
        self.fileHandler.handleFile(self.sourcePath + self.composerJsonFile, destination, self.composerJsonFile, data)


    # handle registration.php file
    def handleRegistrationFile(self):
        destination = os.path.join(self.vendorName, self.moduleName)
        data = {
            'ComponentName': self.componentName
        }
        self.fileHandler.handleFile(self.sourcePath + self.registrationFile, destination, self.registrationFile, data)

    def handleModuleFile(self):
        source = os.path.join(self.sourcePath, self.etcPathFolder, self.moduleFile)
        destination = os.path.join(self.vendorName, self.moduleName, 'etc')
        os.mkdir(destination)
        data = {
            'ComponentName': self.componentName
        }
        self.fileHandler.handleFile(source, destination, self.moduleFile, data)


