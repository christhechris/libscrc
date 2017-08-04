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

webdelchannel   = originInstance.delchannel
webdelitems     = originInstance.delitems
