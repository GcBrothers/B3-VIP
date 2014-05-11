import b3
import b3.plugin
import b3.events
import os
import random

class VipPlugin(b3.plugin.Plugin):
    #Variables
    _currentVip = -1
    _damager = None
    _damaged = None
    _random = False
    def OnStartup(self):
        self.registerEvent(self.console.getEventID('EVT_CLIENT_DAMAGE'), self.onDamage)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_KILL'), self.onKill)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_DISCONNECT'), self.onDisconnect)
        self._adminPlugin = self.console.getPlugin('admin')

        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return
        # Register commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

    def checkIfVip(self):
        self.console.say('Attacker %s Attacked %s'%(self._damager.name, self._damaged.name)) #debug message
        if self._currentVip == self._damaged.cid:
            self.console.write('slap %s'%(self._damager.cid)) #slap if you hit the VIP

    def chooseRandomVip(self): #to choose another people when dead or random mode launched
        clients = self.console.clients.getList()
        i = random.randint(0, len(clients) - 1)
        self._currentVip = clients[i].cid
        clients[i].message('You are the VIP')

#Events

    def onDamage(self, event):
        self._damager = event.attacker
        self._damaged = event.victim
        self.checkIfVip()

    def onKill(self, event):
        if self._random == True:
            if event.victim.cid == self._currentVip:
                self.chooseRandomVip()

    def onDisconnect(self, event):
        if self._random == True:
            if event.client.cid == self._currentVip:
                self.chooseRandomVip()

# Command

    def cmd_vip(self, data, client, cmd = None) #when you configure vip mode
        arg = self._adminPlugin.parseUserCmd(data)
        if not arg:
            client.message('^7 Arguments : Client, off or random') #help message if no arguments
        #argument = self.getReason(args)
        if arg == 'off': #Turns off vip mode
            self._random = False
            self._currentVip = -1
        elif arg == 'random': #set random mode
            self._random = True
            self.chooseRandomVip()
        else: #If a player is chosen to be VIP
            self._random = False
            targetClient = self._adminPlugin.findClientPrompt(arg, client)
            if targetClient:
                self._currentVip = targetClient.cid
                targetClient.message('You are the VIP')
            else:
                client.message('Unable to find %s'%(arg))
