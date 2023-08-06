import requests
from .class_types import nospamplusclass


class Connect:
    """
    Class To Connect Your Token And Use It Efficiently.
    """
    def __init__(self, token: str):
        self.token = token
        self.base = 'http://nospamplus.tk'
        tokencheckurl = 'http://nospamplus.tk' + f'/tokencheck/?token={token}'
        tokencheckrequest = requests.get(url=tokencheckurl).json()
        if tokencheckrequest['token_valid'] is False:
            raise Exception(f'Your Token {token} is Invalid, Check it Again !')
        else:
            pass

    def ban(self, user_id: int, reason: str):
        """
        :param user_id: User id of entity
        :param reason: reason of ban
        :return: Json Object
        Requires Dev Permission
        """
        token = self.token
        userid = user_id
        reason_is = reason
        banuserlink = 'http://nospamplus.tk' + f'/ban/?userid={userid}&ban_code={reason_is}&token={token}'
        banuserrequest = requests.get(url=banuserlink).json()
        if banuserrequest['error'] is True:
            raise Exception('Something Went Wrong While Processing Your Request \nError: ' + banuserrequest['full'])
        else:
            return banuserrequest

    def unban(self, user_id: int):
        """
        :param user_id: User id of entity to unban
        :return: json object if success else raises Exception
        """
        token = self.token
        userid = user_id
        unbanurl = 'http://nospamplus.tk' + f'/unban/?userid={userid}&token={token}'
        unbanrequest = requests.get(url=unbanurl).json()
        if unbanrequest['error'] is True:
            raise Exception('Something Went Wrong While Processing Your Request \nError: ' + unbanrequest['full'])
        else:
            return unbanrequest

    def new_token(self, nospamplustoken: str):
        """
        :param nospamplustoken: Token which should be added
        :return: Json object if success else raises Exception
        """
        tokenz = nospamplustoken
        secret_token = self.token
        newtokenurl = 'http://nospamplus.tk' + f'/newtoken/?token={tokenz}&secrets={secret_token}'
        newtokenrequest = requests.get(url=newtokenurl).json()
        if newtokenrequest['error'] is True:
            raise Exception('Something Went Wrong While Processing Your Request \nError: ' + newtokenrequest['full'])
        else:
            return newtokenrequest

    def is_banned(self, user_id: int):
        """
        :param user_id: userid of entity
        :returns: Ban Class(Object)
        """
        token = self.token
        userid = user_id
        is_it = dict(token=token, userid=userid)
        getbanurl = 'http://nospamplus.tk' + '/info/'
        is_bannedrequest = requests.post(url=getbanurl, data=is_it).json()
        if is_bannedrequest['error'] is True:
            raise Exception('Something Went Wrong While Processing Your Request \nError: ' + is_bannedrequest['full'])
        elif is_bannedrequest['banned'] is False:
            return None
        else:
            return nospamplusclass(**is_bannedrequest)
