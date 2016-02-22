#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from collections import defaultdict

from lib import END


class Response(object):

    def __init__(self, screen, nick, prefix):
        self.screen = screen
        self.nick = nick
        self.prefix_line = prefix
        self.ln_strip = lambda s: s.strip(':')
        self.chan = None
        self.chan_names = defaultdict(list)
        self.comp_chan_names = False
        self.log_links = False
        self.server_cmds = list()

    def whois_user_repl(self, user_data):
        server_repl = 'User: %s' % (user_data[1] + '@' + user_data[2] + '\n')
        self.prefix_line("Server") 
        self.screen.insert(END, server_repl)
        self.screen.see(END)

    def whois_chan_repl(self, chan_data):
        if len(chan_data) != 2: return
        self.prefix_line("Server")
        server_repl = ('Real Name: %s\n' % chan_data[0])
        self.screen.insert(END, server_repl)
        self.prefix_line("Server")
        self.server_repl = ('Server: %s\n' % chan_data[1].strip(':'))
        self.screen.insert(END, server_repl)
        self.screen.see(END)

    def names_repl(self, userlist):
        self.chan = userlist[1] # XXX python3 index error out of range
        self.chan_names[userlist[1]] += map(self.ln_strip, userlist[2:])

    def end_names_repl(self, server_end):
        if self.comp_chan_names and len(self.chan_names) < 2: return
        if not self.comp_chan_names:
            self.prefix_line("Server")
            if not self.chan:
                self.screen.insert(END, "Channel does not exist\n")
            else:
                self.screen.insert(END, "Total Users in %s: %d\n" % 
                                   (self.chan, len(self.chan_names[self.chan])))
                self.screen.insert(END, "%s\n" % ' '.join(self.chan_names[self.chan]))
        else:
            self.comp_chan_names = False
            users = [j for i in self.chan_names.values() for j in i]
            like_users = {i for i in users if users.count(i) > 1}
            self.prefix_line("Server")
            self.screen.insert(END, 'Shared users %d\n' % len(like_users))
            self.screen.insert(END, '%s\n' % ' '.join(like_users))
        self.screen.see(END)
        self.chan = None
        self.chan_names = defaultdict(list)

    def info_repl(self, server_data):
        server_info_repl = ' '.join(map(self.ln_strip, server_data))
        self.prefix_line("Server") 
        self.screen.insert(END, server_info_repl + '\n')
        self.screen.see(END)

    def links_repl(self, server_data):
        link_info = ' '.join(server_data[3:])
        self.prefix_line("Server")
        self.screen.insert(END, link_info + '\n')
        self.screen.see(END)

    def perm_denied_repl(self, server_response):
        server_response = ' '.join(server_response).strip(':')
        self.prefix_line("Server") 
        self.screen.insert(END, server_response + '\n')
        self.screen.see(END)

    def rate_lim_repl(self, server_response):
        server_response = ' '.join(server_response[1:]).strip(':')
        self.prefix_line("Server") 
        self.screen.insert(END, server_response + '\n')
        self.screen.see(END)

    def server_com_repl(self, server_coms):
        self.server_cmds.append(server_coms[0])

    def server_com_end(self, server_end):
        self.prefix_line("Server")
        self.screen.insert(END, "Total Server Commands: %d\n" % 
                                        len(self.server_cmds))
        self.screen.insert(END, "%s\n" % str(self.server_cmds))
        self.screen.see(END)
        self.server_cmds = list()

    def server_con_repl(self, server_connections):
        server_connections = ' '.join(server_connections)
        self.prefix_line("Server") 
        self.screen.insert(END, server_connections + '\n')
        self.screen.see(END)

    def server_utme_repl(self, server_data):
        server_data = ' '.join(server_data[:9]).strip(':')
        self.prefix_line("Server") 
        self.screen.insert(END, server_data + '\n')
        self.screen.see(END)

    def clnt_auth_repl(self, client_data):
        client_data = ' '.join(client_data)
        self.prefix_line("Server") 
        self.screen.insert(END, client_data + '\n')
        self.screen.see(END)

    def server_ver(self, server_data):
        self.prefix_line("Server") 
        self.screen.insert(END, 'Server Version: %s\n' % server_data[0])
        self.screen.see(END)

    def server_aux(self, server_data):
        self.prefix_line("Server") 
        self.screen.insert(END, ' '.join(server_data) + '\n')
        self.screen.see(END)

    def chan_topic(self, topic):
        self.prefix_line("Server") 
        self.screen.insert(END, 'Topic for %s\n' % (' '.join(topic)))
        self.screen.see(END)

    def nick_inuse(self, msg):
        self.prefix_line("Server") 
        self.screen.insert(END, ' '.join(msg[:6]) + '\n')
        self.screen.insert(END, 'Use the /NICK <nick> command to choose a new nick\n')
        self.screen.see(END)

    def list_repl(self, list_data):
        topic = ' '.join(list_data)
        self.prefix_line("Server") 
        self.screen.insert(END, "--" + topic.split(' :')[0] + "--\n")
        try:
            self.screen.insert(END, topic.split(' :')[1] + '\n')
        except IndexError:
            pass
        self.screen.see(END)
        if self.log_links:
            with open(os.getcwd() + '/.link.txt', 'a') as f:
                f.write(('=' * 25) + '\n')
                f.write('--' + topic.split(' :')[0] + '--\n')
                try:
                    f.write(topic.split(' :')[0] + '\n')
                except IndexError:
                    pass
                f.write('\n')

