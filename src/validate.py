# -*- coding: utf-8 -*-

def parse_line(original_line, default_value=''):
    split_name = original_line.split(':', 1)
    if len(split_name) == 2:
        result = split_name[1].strip()
        if len(result) != 0:
            return result
    return default_value


def parse_register_message(message_text, contest_type):
    team_name = ''
    summoner_list = []

    split_text = message_text.split('\n')

    for line in split_text:
        if line.find('チーム名') == 0:
            team_name = parse_line(line)
            if len(team_name) == 0:
                break
        elif line.find('サモナーネーム') == 0:
            summoner_name = parse_line(line)
            if len(summoner_name) == 0:
                break
            else:
                summoner_list.append(summoner_name)
    
    if contest_type == 'solo' and len(summoner_list) != 1:
        print('not solo request.')
        raise
    elif contest_type == 'team5' and len(summoner_list) != 5:
        print('team size is not 5.')
        raise
    elif contest_type == 'team5' and team_name == '':
        print('team name is empty.')
        raise
    else:
        return team_name, summoner_list


def format_accepted_text(contest_name, contest_type, accepted_list):
    result_text = '```' + contest_name + '\n'
    team_name = ''
    summoner_number = 1

    for summoner in accepted_list:
        if contest_type == 'solo':
            result_text = result_text + summoner[1] + '\n'
        elif contest_type == 'team5' and team_name != summoner[0]:
            team_name = summoner[0]
            result_text = result_text + '■ ' + team_name + '\n'
            result_text = result_text + summoner[1] + ','
            summoner_number += 1
        elif contest_type == 'team5':
            if summoner_number != 5:
                result_text = result_text + summoner[1] + ','
                summoner_number += 1
            else:
                result_text = result_text + summoner[1] + '\n'
                summoner_number = 1

    return result_text + '```'
