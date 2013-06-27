#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import *


class Response(object):

    def __init__(self, screen, nick, prefix):
        self.screen = screen
        self.nick = nick
        self.prefix_line = prefix

    def whois_user_repl(self, user_data):
        server_repl = 'User: %s' % (user_data[1] + '@' + user_data[2] + '\n')
        self.prefix_line("Server") 
        self.screen.insert(END, server_repl)
        self.screen.see(END)

    def whois_chan_repl(self, chan_data):
        if len(chan_data) == 2:
            self.prefix_line("Server")
            server_repl = ('Real Name: %s\n' % chan_data[0])
            self.screen.insert(END, server_repl)
            self.prefix_line("Server")
            self.server_repl = ('Server: %s\n' % chan_data[1].strip(':'))
            self.screen.insert(END, server_repl)
            self.screen.see(END)

    def names_repl(self, userlist):
        if any(i.endswith('.freenode.net') for i in userlist[2:]):
            pass
        else:
            server_repl = ('Users available on %s:\n' + '=' * 25 + '\n') % userlist[1]
            for usr in userlist[2:]:
                server_repl += ('  ~' + usr.strip(':@') + '\n')
            self.prefix_line("Server") 
            self.screen.insert(END, server_repl)
            self.screen.see(END)

    def info_repl(self, server_data):
        server_data = ' '.join(i.strip(':') for i in server_data)
        self.prefix_line("Server") 
        self.screen.insert(END, server_data + '\n')
        self.screen.see(END)

    def links_repl(self, server_data):
        link_info = ' '.join(i for i in server_data[3:])
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
        self.prefix_line("Server") 
        self.screen.insert(END, '%s\n' % server_coms[0])
        self.screen.see(END)

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
