from .PBoxWebAPI import PBoxWebAPI


instanceList = []

def new_instance():
    newInstance = PBoxWebAPI()
    instanceList.append(newInstance)
    return newInstance

originInstance = new_instance()

weblogin   = originInstance.login

webnewchannel   = originInstance.newchannel
webnewdevice    = originInstance.newdevice
webnewitem      = originInstance.newitem
webnewitems     = originInstance.newitems

webalterchannel = originInstance.alterchannel
webalterdevice  = originInstance.alterdevice
webalteritem    = originInstance.alteritem

webdelchannel   = originInstance.delchannel
webdelitems     = originInstance.delitems

webcloudaddress = originInstance.cloudaddress
webdownload     = originInstance.download2app
armreboot       = originInstance.reboot

webnewpassword  = originInstance.newpassword
weblanip        = originInstance.lanipaddress
