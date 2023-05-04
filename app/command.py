#!/usr/bin/python
#Copyright (c) by linhtx
# -*- coding: utf-8 -*-
import os
import shutil
import re
from app.file_handler import FileHandler

class Command:

    def __init__(self, vendorName, moduleName, componentName, commandData, newOrderStatus, paymentCode):
        self.vendorName = vendorName
        self.componentName = componentName
        self.moduleName = moduleName
        self.commandData = commandData
        self.newOrderStatus = newOrderStatus
        self.paymentCode = paymentCode
        self.fileHandler = FileHandler()
        self.httpPath = 'Http'
        self.clientPath = 'Client'
        self.gatewayPath = 'Gateway'
        self.fullGatewayPath = os.path.join(self.vendorName, self.moduleName, self.gatewayPath)
        self.requestPath = 'Request'
        self.responsePath = 'Response'
        self.validatorPath = 'Validator'
        self.requestFile = 'RequestBuilderData.php'
        self.handlerFile = 'Handler.php'
        self.validatorFile = 'Validator.php'
        self.transferFactoryFile = 'TransferFactory.php'
        self.clientFile = 'Client.php'
        self.initialize = 'initialize'
        self.capture = 'capture'
        self.authorize = 'authorize'
        self.void = 'void'
        self.refund = 'refund'
        self.fetch = 'fetch'
        self.sourcePath = 'source/'
        self.etcPath = 'etc'
        self.configXmlFile = 'config.xml'
        self.commandDeclaration = '<item name="command" xsi:type="string">CommandDeclarationName</item>'
        self.header = '''
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
'''
        self.footer = '''
</config>
'''
        self.facade = '''
    <!-- Payment Method Facade configuration ModuleName -->
    <virtualType name="ModuleNameFacade" type="Magento\Payment\Model\Method\Adapter">
    <arguments>
        <argument name="code" xsi:type="const">VendorName\ModuleName\Gateway\Config\Config::CODE</argument>
        <argument name="formBlockType" xsi:type="string">Magento\Payment\Block\Form</argument>
        <argument name="infoBlockType" xsi:type="string">Magento\Payment\Block\ConfigurableInfo</argument>
        <argument name="valueHandlerPool" xsi:type="object">ModuleNameValueHandlerPool</argument>
        <argument name="commandPool" xsi:type="object">ModuleNameCommandPool</argument>
    </arguments>
    </virtualType>
'''
        self.commandPool = '''
    <!-- Commands infrastructure ModuleName -->
    <virtualType name="ModuleNameCommandPool" type="Magento\Payment\Gateway\Command\CommandPool">
        <arguments>
            <argument name="commands" xsi:type="array">
                command_pool_declaration
            </argument>
        </arguments>
    </virtualType>
'''
        self.initializeCommand = '''
    <!--Initialize Command-->
    <virtualType name="ModuleNameInitializeCommand" type="Magento\Payment\Gateway\Command\GatewayCommand">
        <arguments>
            <argument name="transferFactory" xsi:type="object">VendorName\ModuleName\Gateway\Http\TransferFactory</argument>
            <argument name="client" xsi:type="object">VendorName\ModuleName\Gateway\Http\Client\Client</argument>
            <argument name="requestBuilder" xsi:type="object">ModuleNameInitializeRequestBuilder</argument>
            <argument name="handler" xsi:type="object">VendorName\ModuleName\Gateway\Response\InitializeHandler</argument>
            <argument name="validator" xsi:type="object">VendorName\ModuleName\Gateway\Validator\Validator</argument>
        </arguments>
    </virtualType>

    <virtualType name="ModuleNameInitializeRequestBuilder" type="Magento\Payment\Gateway\Request\BuilderComposite">
        <arguments>
            <argument name="builders" xsi:type="array">
                <item name="payment_code_initialize_request_data" xsi:type="string">VendorName\ModuleName\Gateway\Request\InitializeRequestBuilderData</item>
            </argument>
        </arguments>
    </virtualType>
'''

        self.captureCommand = '''
    <!-- Capture Command -->
    <virtualType name="ModuleNameCaptureCommand" type="Magento\Payment\Gateway\Command\GatewayCommand">
        <arguments>
            <argument name="transferFactory" xsi:type="object">VendorName\ModuleName\Gateway\Http\TransferFactory</argument>
            <argument name="client" xsi:type="object">VendorName\ModuleName\Gateway\Http\Client\Client</argument>
            <argument name="requestBuilder" xsi:type="object">ModuleNameCaptureRequestBuilder</argument>
            <argument name="handler" xsi:type="object">VendorName\ModuleName\Gateway\Response\CaptureHandler</argument>
            <argument name="validator" xsi:type="object">VendorName\ModuleName\Gateway\Validator\Validator</argument>
        </arguments>
    </virtualType>

    <virtualType name="ModuleNameCaptureRequestBuilder" type="Magento\Payment\Gateway\Request\BuilderComposite">
        <arguments>
            <argument name="builders" xsi:type="array">
                <item name="payment_code_capture_request_data" xsi:type="string">VendorName\ModuleName\Gateway\Request\CaptureRequestBuilderData</item>
            </argument>
        </arguments>
    </virtualType>
'''
        self.authorizeCommand = '''
    <!-- Authorize Command-->
    <virtualType name="ModuleNameAuthorizeCommand" type="Magento\Payment\Gateway\Command\GatewayCommand">
        <arguments>
            <argument name="transferFactory" xsi:type="object">VendorName\ModuleName\Gateway\Http\TransferFactory</argument>
            <argument name="client" xsi:type="object">VendorName\ModuleName\Gateway\Http\Client\Client</argument>
            <argument name="requestBuilder" xsi:type="object">ModuleNameAuthorizeRequestBuilder</argument>
            <argument name="handler" xsi:type="object">VendorName\ModuleName\Gateway\Response\AuthorizeHandler</argument>
            <argument name="validator" xsi:type="object">VendorName\ModuleName\Gateway\Validator\Validator</argument>
        </arguments>
    </virtualType>

    <virtualType name="ModuleNameAuthorizeRequestBuilder" type="Magento\Payment\Gateway\Request\BuilderComposite">
        <arguments>
            <argument name="builders" xsi:type="array">
                <item name="payment_code_authorize_request_data" xsi:type="string">VendorName\ModuleName\Gateway\Request\AuthorizeRequestBuilderData</item>
            </argument>
        </arguments>
    </virtualType>
'''

        self.voidCommand = '''
    <!-- Void Command-->
    <virtualType name="ModuleNameVoidCommand" type="Magento\Payment\Gateway\Command\GatewayCommand">
        <arguments>
            <argument name="transferFactory" xsi:type="object">VendorName\ModuleName\Gateway\Http\TransferFactory</argument>
            <argument name="client" xsi:type="object">VendorName\ModuleName\Gateway\Http\Client\Client</argument>
            <argument name="requestBuilder" xsi:type="object">ModuleNameVoidRequestBuilder</argument>
            <argument name="handler" xsi:type="object">VendorName\ModuleName\Gateway\Response\VoidHandler</argument>
            <argument name="validator" xsi:type="object">VendorName\ModuleName\Gateway\Validator\Validator</argument>
        </arguments>
    </virtualType>

    <virtualType name="ModuleNameVoidRequestBuilder" type="Magento\Payment\Gateway\Request\BuilderComposite">
        <arguments>
            <argument name="builders" xsi:type="array">
                <argument name="payment_code_void_request_data" xsi:type="object">VendorName\ModuleName\Gateway\Request\VoidRequestBuilderData</argument>
            </argument>
        </arguments>
    </virtualType>
'''
        self.refundCommand = '''
    <!-- Refund Command -->
    <virtualType name="ModuleNameRefundCommand" type="Magento\Payment\Gateway\Command\GatewayCommand">
        <arguments>
            <argument name="transferFactory" xsi:type="object">VendorName\ModuleName\Gateway\Http\TransferFactory</argument>
            <argument name="client" xsi:type="object">VendorName\ModuleName\Gateway\Http\Client\Client</argument>
            <argument name="requestBuilder" xsi:type="object">ModuleNameRefundRequestBuilder</argument>
            <argument name="handler" xsi:type="object">VendorName\ModuleName\Gateway\Response\RefundHandler</argument>
            <argument name="validator" xsi:type="object">VendorName\ModuleName\Gateway\Validator\Validator</argument>
        </arguments>
    </virtualType>

    <virtualType name="ModuleNameRefundRequestBuilder" type="Magento\Payment\Gateway\Request\BuilderComposite">
        <arguments>
            <argument name="builders" xsi:type="array">
                <argument name="payment_code_refund_request_data" xsi:type="object">VendorName\ModuleName\Gateway\Request\RefundRequestBuilderData</argument>
            </argument>
        </arguments>
    </virtualType>
'''
        self.fetchCommand = '''
    <!-- Fetch Transaction Information Command-->
    <virtualType name="ModuleNameFetchCommand" type="Magento\Payment\Gateway\Command\GatewayCommand">
        <arguments>
            <argument name="transferFactory" xsi:type="object">VendorName\ModuleName\Gateway\Http\TransferFactory</argument>
            <argument name="client" xsi:type="object">VendorName\ModuleName\Gateway\Http\Client\Client</argument>
            <argument name="requestBuilder" xsi:type="object">ModuleNameFetchRequestBuilder</argument>
            <argument name="handler" xsi:type="object">VendorName\ModuleName\Gateway\Response\FetchHandler</argument>
            <argument name="validator" xsi:type="object">VendorName\ModuleName\Gateway\Validator\Validator</argument>
        </arguments>
    </virtualType>

    <virtualType name="ModuleNameFetchRequestBuilder" type="Magento\Payment\Gateway\Request\BuilderComposite">
        <arguments>
            <argument name="builders" xsi:type="array">
                <argument name="payment_code_fetch_request_data" xsi:type="object">VendorName\ModuleName\Gateway\Request\FetchRequestBuilderData</argument>
            </argument>
        </arguments>
    </virtualType>
'''
        self.commandDiList = {
            self.initialize: self.initializeCommand,
            self.authorize: self.authorizeCommand,
            self.capture: self.captureCommand,
            self.void: self.voidCommand,
            self.refund: self.refundCommand,
            self.fetch: self.fetchCommand
        }
        self.handleDiFile()
        self.handleHttpFolder()
        self.handlePhpCommandFile()
        self.handleConfigXml()

    def handlePhpCommandFile(self):
        for command in self.commandData:
            data = {
                'VendorName': self.vendorName,
                'ModuleName': self.moduleName,
                'CommandName': command.capitalize()
            }
            self.handleRequest(command, data)
            self.handleHandler(command, data)
            self.handleValidator(data)

    def handleRequest(self, commandName,data):
        self.handlePhpFile(self.requestPath, self.requestFile, commandName.capitalize() + self.requestFile, data)

    def handleHandler(self, commandName, data):
        self.handlePhpFile(self.responsePath, self.handlerFile, commandName.capitalize() + self.handlerFile, data)

    def handleValidator(self, data):
        self.handlePhpFile(self.validatorPath, self.validatorFile, self.validatorFile, data)

    def handlePhpFile(self, path, sourceFile, resultFile, data):
        destination = os.path.join(self.fullGatewayPath, path)
        if  not os.path.exists(destination):
            os.mkdir(destination)
        source = os.path.join(self.sourcePath, self.gatewayPath, path, sourceFile)
        self.fileHandler.handleFile(source, destination, resultFile, data)

    def handleDiFile(self):
        filePath = os.path.join(self.vendorName, self.moduleName, self.etcPath)
        diData = {
            'VendorName': self.vendorName,
            'ModuleName': self.moduleName,
            'payment_code': self.paymentCode
        }
        commandDeclarationList = []
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        with open(filePath + '/di.xml', 'w') as file:
            fullText = self.header + self.facade + self.commandPool
            for selectedCommand in self.commandData:
                fullText += self.commandDiList[selectedCommand]
                if selectedCommand == 'fetch':
                    selectedCommand = 'fetch_transaction_information'
                commandDeclarationList.append(self.commandDeclaration.replace(
                    'command', selectedCommand
                    ).replace(
                    'CommandDeclarationName', self.moduleName + selectedCommand.capitalize() + 'Command'
                    ))
            fullText += self.footer
            diData['command_pool_declaration'] = '\n\t\t\t\t'.join(commandDeclarationList)
            for data in diData:
                fullText = fullText.replace(data, diData[data])
            file.write(fullText)

    def handleHttpFolder(self):

        sourceTransferFactory = os.path.join(self.sourcePath, self.gatewayPath, self.httpPath, self.transferFactoryFile)
        destinationTransferFactory = os.path.join(self.vendorName, self.moduleName, self.gatewayPath, self.httpPath)
        sourceClient = os.path.join(self.sourcePath, self.gatewayPath, self.httpPath, self.clientPath, self.clientFile)
        destinationClient = os.path.join(self.vendorName, self.moduleName, self.gatewayPath, self.httpPath, self.clientPath)
        data = {
            'VendorName': self.vendorName,
            'ModuleName': self.moduleName
        }
        self.fileHandler.handleFile(sourceTransferFactory, destinationTransferFactory, self.transferFactoryFile, data)
        self.fileHandler.handleFile(sourceClient, destinationClient, self.clientFile, data)

    def handleConfigXml(self):
        source = os.path.join(self.sourcePath, self.etcPath, self.configXmlFile)
        destination = os.path.join(self.vendorName, self.moduleName, self.etcPath)
        commandList = {
            'can_initialize_variable': '0',
            'can_capture_variable': '0',
            'can_authorize_variable': '0',
            'can_void_variable': '0',
            'can_refund_variable': '0',
            'can_fetch_variable': '0'
        }
        for command in self.commandData:
            key = 'can_' + command + '_variable'
            commandList[key] = '1'

        data = {
            'ModuleName': self.moduleName,
            'payment_title': re.sub(r"(\w)([A-Z])", r"\1 \2", self.moduleName),
            'new_order_status': self.newOrderStatus
        }
        data.update(commandList)
        self.fileHandler.handleFile(source, destination, self.configXmlFile, data)
