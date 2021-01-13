def setIdmPath():
    import os
    idmPath = open('idm_path.dat').readline().strip()
    command = 'SETX IDM_PATH "%s"' % idmPath
    os.system(command)

setIdmPath()
