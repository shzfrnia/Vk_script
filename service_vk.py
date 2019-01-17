#!/usr/local/bin/python3

import os
import requests
import account
from dotenv import load_dotenv


load_dotenv()


class ServiceVk:
    __ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN")
    __VK_API = "https://api.vk.com/method/"
    __API_VERSION = "5.80"
    __LANGUAGE = "ru"

    def request_info_of_account(self, vk_account_id):
        account_info = self.__request_json("users.get", params={"user_ids": vk_account_id,
                                                                "fields": "online"})["response"][0]
        vk_user = account.Account(account_info)
        return vk_user

    def check_id_on_exists(self, vk_account_ids):
        request_info_of_user = self.__request_json(
            "users.get", params={"user_ids": vk_account_ids})
        if "error" in request_info_of_user:
            raise IOError(request_info_of_user["error"]["error_msg"])
        elif not request_info_of_user["response"]:
            raise IOError("Sorry but account isn't exists")
        elif "deactivated" in request_info_of_user["response"][0]:
            raise IOError("Try again this account is: " +
                          request_info_of_user["response"][0]["deactivated"])
        return True

    def __request_json(self, method, params):
        vk_method = self.__VK_API + str(method)
        vk_access_token = "?access_token=" + self.__ACCESS_TOKEN
        vk_api_v = "&v=" + self.__API_VERSION
        vk_lang = "&lang=" + self.__LANGUAGE
        req = requests.get(vk_method + vk_access_token +
                           vk_api_v + vk_lang, params)
        json_data = req.json()
        return json_data

    def requests_public_friend_list(self, vk_account_id, fields="online"):
        parametrs = {"order": "name",
                     "fields": fields,
                     "user_id": vk_account_id}
        req = self.__request_json("friends.get", parametrs)
        friends_list = req["response"]["items"]

        friends_list = list(map(account.Account, friends_list))
        return friends_list