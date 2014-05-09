import b3
import b3.plugin
import b3.events
import os

class VipPlugin(b3.plugin.Plugin):
    #Variables
    currentVip = -1
    damager = None
    damaged = None
    def OnStartup(self):
        self.registerEvent(b3.events.EVT_CLIENT_DAMAGE)
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
        self.console.say('Attacker %s Attacked %s'%(damager.name, damaged.name)) #debug message
        if currentVip == damaged.cid
            self.console.write('slap %s'%(damager.cid)) #slap if you hit VIP
    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_DAMAGE: #get who hits, and who's hit
            damager = event.attacker
            damaged = event.victim
            self.checkIfVip()
    def cmd_vip(self, data, client, cmd = None) #when you configure vip mode
        arg = self._adminPlugin.parseUserCmd(data)
        if not arg:
            client.message('^7 Arguments : Client, off or random') #help message if no arguments

        #argument = self.getReason(args)
        if arg == 'off': #Turns off vip mode
            targetClient = -1
        else: #Tell new Vip
            targetClient = getClientByName(arg) #or getClientLikeName(argument) ?
            if targetClient:
                currentVip = targetClient.cid
                targetClient.message('You are the VIP')
            else:
                client.message('Unable to find %s'%(arg))
