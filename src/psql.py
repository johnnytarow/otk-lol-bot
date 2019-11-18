# -*- coding: utf-8 -*-

import db_connector as db
import config
# import local_config as config
from datetime import datetime

REGISTER_USER_QUERY = 'insert into register_user (contest_name, team_name, discord_id, summoner_name, register_time) values (%s, %s, %s, %s, now())'
GET_USER_QUERY = 'select * from register_user where contest_name = %s and summoner_name = %s'
GET_TEAM_QUERY = 'select * from register_user where team_name != \'\' and team_name = %s'
GET_DISCORD_ID_QUERY = 'select * from register_user where contest_name = %s and discord_id = %s'

GET_ACCEPT_MESSAGE_QUERY = 'select message_id from registered_message where contest_name = %s'
GET_ACCEPT_SUMMONER_QUERY = 'select team_name, summoner_name from register_user where contest_name = %s order by team_name, register_time'
DELETE_ACCEPT_MESSAGE_QUERY = 'delete from registered_message where contest_name = %s'
INSERT_ACCEPT_MESSAGE_QUERY = 'insert into registered_message (contest_name, message_id) values (%s, %s)'


def execute_select_query(query, parameter):
    with db.DatabaseConnector(config.DB_ACCOUNT) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, parameter)
                result = cursor.fetchall()
                return result
            except:
                print('error: ' + query)
                raise


def execute_update_query(delete_query, insert_query, delete_parameter, insert_parameter):
    with db.DatabaseConnector(config.DB_ACCOUNT) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(delete_query, delete_parameter)
                cursor.execute(insert_query, insert_parameter)
                conn.commit()
                return True
            except:
                print('error: ' + insert_query)
                raise


def register_user(contest_name, team_name, discord_id, summoner_list):
    is_exist_team_name = execute_select_query(GET_TEAM_QUERY, [team_name])
    is_exist_discord_id = execute_select_query(GET_DISCORD_ID_QUERY, [contest_name, discord_id])
    if is_exist_team_name or is_exist_discord_id:
        print('already registered.')
        raise
    else:
        with db.DatabaseConnector(config.DB_ACCOUNT) as conn:
            with conn.cursor() as cursor:
                for summoner in summoner_list:
                    try:
                        # summoner already registered
                        cursor.execute(GET_USER_QUERY, [contest_name, summoner])
                        is_exist = cursor.fetchone()
                        if is_exist:
                            print(is_exist)
                            print('already registered.')
                            raise
                    except:
                        print('error: check already registerd.')
                        raise
                    
                    try:
                        # register
                        cursor.execute(REGISTER_USER_QUERY, [contest_name, team_name, discord_id, summoner])
                        result = True
                    except:
                        print('error: register user.')
                        raise
            if result:
                conn.commit()
            else:
                conn.rollback()
    return result


def get_accepted_message(contest_name):
    result = execute_select_query(GET_ACCEPT_MESSAGE_QUERY, [contest_name])
    if result:
        message_id = result[0][0]
        return message_id
    else:
        print('not write accepted message yet.')
        return None


def get_accept_summoner(contest_name):
    result = execute_select_query(GET_ACCEPT_SUMMONER_QUERY, [contest_name])
    if result:
        return result
    else:
        print('no accept user.')
        return None


def update_accepted_message(contest_name, accepted_message_id):
    result = execute_update_query(DELETE_ACCEPT_MESSAGE_QUERY, INSERT_ACCEPT_MESSAGE_QUERY, [contest_name], [contest_name, accepted_message_id])
    if result:
        return True
    else:
        print('fail to update accepted message info.')
        raise
