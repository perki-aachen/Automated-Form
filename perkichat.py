#! /usr/bin/env python3
import requests
import datetime
import yaml
##------------------------Global Variables-------------------------------##

URL = "https://notify-api.line.me/api/notify"


class PerkiChat:
    
    """
    Class for chating in line messenger.

    ...

    Attributes
    ----------
    mode : str
        mode for chatting depends on the token, i.e., personal, perki, tests

    Methods
    -------
    getToken:
        Get token and choose channel for chat
        
    send_message
    """

    
    
    def __init__(self, mode, sender):
        
        """
        Parameters
        ----------
        mode : str
            The token mode 
        """
        
        self.mode = mode
        self.sender = sender
        
    
    def getToken(self):
        
        """
        Get the token from yaml file
 
        """
        from pathlib import Path
        token_fn = Path(__file__).resolve().parent / 'YAML' / 'token.yaml' 
        token_file = open(token_fn, "r")
        parsed_yaml = yaml.load(token_file, Loader=yaml.FullLoader)
        self.token = parsed_yaml[self.sender][self.mode]

    def send_message(self, msg, img=None):
        
        """
        Send a message to specific channel

        Parameters
        ----------
        msg : str
            The message to be sent
        img : str
            Path to open the image (default :None)
        
        """
        ## run script getToken
        self.getToken()
        ## send mesage
        message = {'message': msg}
        LINE_HEADERS = {'Authorization': 'Bearer ' + self.token}
        files = {'imageFile': open(img, 'rb')} if img else None
        session = requests.Session()
        resp = session.post(URL, headers=LINE_HEADERS, params=message, files=files)
        if files:
            files['imageFile'].close()
        self.status = resp.status_code
