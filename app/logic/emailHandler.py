from flask import Flask, request, render_template
import yaml, os
from flask_mail import Mail, Message
# from app.config
# from app.config.production import *
from app.models.emailTemplate import EmailTemplate
from app import app
import sys
from pathlib import Path


#borrowed from emailHandler file (and other places) in lsf

def load_config(file):
    """ This should be in a seperate file. prob in the config dir"""
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg

class emailHandler():
    def __init__(self, emailInfo):
        default = load_config('app/config/default.yml')
        app.config.update(
            MAIL_SERVER=default['mail']['server'],
            MAIL_PORT=default['mail']['port'],
            MAIL_USERNAME= default['mail']['username'],
            MAIL_PASSWORD= default['mail']['password'],
            REPLY_TO_ADDRESS= default['mail']['reply_to_address'],
            MAIL_USE_TLS=default['mail']['tls'],
            MAIL_USE_SSL=default['mail']['ssl'],
            MAIL_DEFAULT_SENDER=default['mail']['default_sender'],
            MAIL_OVERRIDE_ALL=default['mail']['override_addr'],
            #ALWAYS_SEND_MAIL=default['ALWAYS_SEND_MAIL']
        )

        self.mail = Mail(app)

    def send(self, message: Message):

        #message.html = "<b>Original message intended for {}.</b><br>".format(", ".join(message.recipients)) + message.html
        message.reply_to = app.config["REPLY_TO_ADDRESS"]
        self.mail.send(message)
        message.recipients = [app.config['MAIL_OVERRIDE_ALL']]
        self.mail.send(message)

        #elif app.config['ENV'] == 'testing':
         #   # TODO: we really should have a way to check that we're sending emails that doesn't spam the logs
          #  message.reply_to = app.config["REPLY_TO_ADDRESS"]
           # self.mail.send(message)
           # print("I did a thing in testing")##############################################################################################
            #pass
        #else:
         #   print("ENV: {}. Email not sent to {}, subject '{}'.".format(app.config['ENV'], message.recipients, message.subject))

        print("emails are being something'ed")#######################################################################################
