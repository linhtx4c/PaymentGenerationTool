#!/usr/bin/python
#Copyright (c) by linhtx
# -*- coding: utf-8 -*-
import os
import re
from app.file_handler import FileHandler

class Payment:
    def __init__(self, vendorName, moduleName, componentName, paymentCode):
        self.paymentCode = paymentCode
        self.vendorName = vendorName
        self.componentName = componentName
        self.moduleName = moduleName
        self.paymentCodeWithHyphen = paymentCode.replace('_', '-')
        self.fileHandler = FileHandler()
        self.sourcePath = 'source/'
        self.etcPath = 'etc'
        self.commonViewPath = 'view/frontend/js/view/payment/'
        self.viewHtmlPath = 'view/frontend/template/payment'
        self.configXmlFile = 'config.xml'
        self.jsPaymentFileName = 'payment-code.js'
        self.htmlPaymentFileName = 'payment_code.html'
        self.configPath = 'Gateway/Config'
        self.configFile = 'Config.php'
        self.modelPath = 'Model'
        self.systemXmlFile = 'system.xml'
        self.adminhtmlPath = 'adminhtml'
        self.diXmlFile = 'di.xml'
        self.frontendPath = 'frontend'
        self.configProviderFile = 'ConfigProvider.php'
        if self.paymentCode != '':
            self.generatePayment()
    
    
    def generatePayment(self):
        self.handeViewFolder()
        self.handleSystemXmlFile()

    def handeViewFolder(self):
        self.handleJsFolder()
        self.handleHtmlFolder()
        self.handleConfigFile()
        self.handleConfigProviderFile()

    def handleJsFolder(self):
        sourcePaymentJsFile = self.sourcePath + self.commonViewPath + self.jsPaymentFileName
        destinationPaymentJsFile = os.path.join(self.vendorName, self.moduleName,  self.commonViewPath)
        sourceMethodRendererJsFile = self.sourcePath + self.commonViewPath + 'method-renderer/' + self.jsPaymentFileName
        destinationMethodRendererJsFile = self.vendorName + '/' + self.moduleName + '/' + self.commonViewPath + 'method-renderer/'
        data = {
            'ComponentName': self.componentName,
            'payment_code': self.paymentCode
        }
        self.fileHandler.handleFile(sourcePaymentJsFile, destinationPaymentJsFile, self.paymentCodeWithHyphen + '.js', data)
        self.fileHandler.handleFile(sourceMethodRendererJsFile, destinationMethodRendererJsFile, self.paymentCodeWithHyphen + '.js', data)

    def handleHtmlFolder(self):
        source = os.path.join(self.sourcePath, self.viewHtmlPath, self.htmlPaymentFileName)
        destination = os.path.join(self.vendorName, self.moduleName,  self.viewHtmlPath)
        self.fileHandler.copyFile(source, destination, self.paymentCode + '.html')

    def handleConfigFile(self):
        source = os.path.join(self.sourcePath, self.configPath, self.configFile)
        destination = os.path.join(self.vendorName, self.moduleName, self.configPath)
        data = {
            'VendorName': self.vendorName,
            'ModuleName': self.moduleName,
            'payment_code': self.paymentCode
        }
        self.fileHandler.handleFile(source, destination, self.configFile, data)

    def handleConfigProviderFile(self):
        source = os.path.join(self.sourcePath, self.modelPath, self.configProviderFile)
        destination = os.path.join(self.vendorName, self.moduleName, self.modelPath)
        data = {
            'VendorName': self.vendorName,
            'ModuleName': self.moduleName
        }
        self.fileHandler.handleFile(source, destination, self.configProviderFile, data)
        self.handleDiConfigProvider()

    def handleDiConfigProvider(self):
        source = os.path.join(self.sourcePath, self.etcPath, self.frontendPath, self.diXmlFile)
        destination = os.path.join(self.vendorName, self.moduleName, self.etcPath, self.frontendPath)
        data = {
            'VendorName': self.vendorName,
            'ModuleName': self.moduleName,
            'payment_code': self.paymentCode
        }
        self.fileHandler.handleFile(source, destination, self.diXmlFile, data)


    def handleSystemXmlFile(self):
        source = os.path.join(self.sourcePath, self.etcPath, self.adminhtmlPath, self.systemXmlFile)
        destination = os.path.join(self.vendorName, self.moduleName, self.etcPath, self.adminhtmlPath)
        paymentTitle = re.sub(r"(\w)([A-Z])", r"\1 \2", self.moduleName)
        data = {
            'payment_code': self.paymentCode,
            'payment_title': paymentTitle
        }
        self.fileHandler.handleFile(source, destination, self.systemXmlFile, data)
