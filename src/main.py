# -*- coding: utf-8 -*-

import sys
import discord

import validate
import psql
import config
# import local_config as config
import config_message

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    guild = client.guilds[0]
    channel_id = message.channel.id
    discord_id = message.author.id
    message_text = message.content

    # for debug
    print(message_text)

    # command for owner
    if channel_id == config.ADMIN_DM_CHANNEL:
        # terminate bot
        if message_text == 'exit':
            await client.logout()
            await sys.exit()
        elif 'refresh_accepted_list' in message_text:
            contest_name = message_text.split(' ', 1)[1]
            for contest_info in config.REGISTER_CHANNELS.values():
                if contest_info['name'] == contest_name:
                    contest_type = contest_info['type']
                    break

            # update accepted message
            message_id = psql.get_accepted_message(contest_name)
            accepted_list = psql.get_accept_summoner(contest_name)

            if accepted_list:
                accepted_text = validate.format_accepted_text(contest_name, contest_type, accepted_list)

                channel = client.get_channel(config.ACCEPT_LIST_CHANNEL)
                if message_id:
                    old_message = await channel.fetch_message(message_id)
                    await old_message.delete()
                    
                accepted_message = await channel.send(accepted_text)
                psql.update_accepted_message(contest_name, accepted_message.id)


    # user registration
    elif str(channel_id) in config.REGISTER_CHANNELS.keys():
        try:
            contest_name = config.REGISTER_CHANNELS[str(channel_id)]['name']
            contest_type = config.REGISTER_CHANNELS[str(channel_id)]['type']

            # varidation message
            team_name, summoner_list = validate.parse_register_message(message_text, contest_type)

            if summoner_list:
                # register
                psql.register_user(contest_name, team_name, discord_id, summoner_list)
                print('registered.')

                # update accepted message
                message_id = psql.get_accepted_message(contest_name)
                accepted_list = psql.get_accept_summoner(contest_name)

                if accepted_list:
                    accepted_text = validate.format_accepted_text(contest_name, contest_type, accepted_list)

                    channel = client.get_channel(config.ACCEPT_LIST_CHANNEL)
                    if message_id:
                        old_message = await channel.fetch_message(message_id)
                        await old_message.delete()
                    
                    accepted_message = await channel.send(accepted_text)
                    psql.update_accepted_message(contest_name, accepted_message.id)
                print('update accepted message.')

                # delete message
                await message.delete()

                # send success message
                success_message = await message.channel.send(config_message.REGISTER_SUCCESS.format(discord_id))
                await success_message.delete(delay=5)
        except:
            # delete message
            fail_message = await message.channel.send(config_message.REGISTER_FAIL.format(discord_id))
            await message.delete(delay=10)
            await fail_message.delete(delay=10)


def main():
    client.run(config.TOKEN)


if __name__ == '__main__':
    main()
