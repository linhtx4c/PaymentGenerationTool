#!/usr/bin/python
#Copyright (c) by linhtx
# -*- coding: utf-8 -*-
import gi
import re
from app.module import Module
from app.payment import Payment
from app.command import Command

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Main(Gtk.Window):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("GeneratePaymentTool.glade")
        self.commandList = []
        self.initialize = 'initialize'
        self.capture = 'capture'
        self.authorize = 'authorize'
        self.void = 'void'
        self.refund = 'refund'
        self.fetch = 'fetch'
        self.commandTypeList = ['request', 'handler', 'validate']
        self.commandNameList = [self.initialize, self.capture, self.authorize, self.void, self.refund, self.fetch]

        window = self.builder.get_object("WindowApplication")
        window.connect("delete-event", Gtk.main_quit)
        window.show()

        generationButton = self.builder.get_object("GererateButton")
        generationButton.connect('clicked', self.on_GererateButton_clicked)

        for commandName in self.commandNameList:
            command = self.builder.get_object(commandName)
            command.connect('toggled', self.selectCommand, commandName)

    def on_GererateButton_clicked(self, button):
        componentName = ''.join(self.builder.get_object('module-name').get_text().split())
        paymentCode = ''.join(self.builder.get_object('payment-code').get_text().split())
        newOrderStatus = ''.join(self.builder.get_object('new-order-status').get_text().split())
        moduleNameArray = componentName.split('_')
        vendorName = ''
        moduleName = ''
        pattern = re.compile('[A-Za-z]+_[A-Za-z]+')
        try:
            if (len(moduleNameArray) > 1 and pattern.match(componentName)):
                vendorName = moduleNameArray[0]
                moduleName = moduleNameArray[1]
                Module(vendorName, moduleName, componentName)
                print('Generate Module Done')
                pattern = re.compile('[a-z]+_[a-z]+')
                if (paymentCode != '' and pattern.match(paymentCode)): 
                    Payment(vendorName, moduleName, componentName, paymentCode)
                    Command(vendorName, moduleName, componentName, self.commandList, newOrderStatus)
                    print('Generate Payment Done')
                else:
                    print('Payment Code is invalid')
            else:
                print('Module Name is invalid')
        except Exception as e:
            print('Something went wrong')
            print(str(e))



    def selectCommand(self, commandSelected, commandName):
        if(commandSelected.get_active()):                
            self.commandList.append(commandName)
        else:
            self.commandList.remove(commandName)

if __name__ == '__main__':
    main = Main()
    Gtk.main()