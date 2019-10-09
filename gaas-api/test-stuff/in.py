som = [('SV_HOSTNAME', 'adakdjaldalksdhalksdjhlh'), ('SV_PASSWORD', 'lkahsdladlkahsdlkahdlh'), ('RCON_PASSWORD', 'lhalsdkajdhkaljshdlkahjdklajhdkahsdlkj'), ('SERVER_TOKEN', 'hlkhalkdshaldhladlahdalhlaadadhadaldhlalhd')]

tests = ["SV_HOSTNAMe","RCON_PASSWORD"]

validated = 0

for arg in tests:
    validated = 0
    for i in som:
        if arg in i:
            validated = 1
            continue
            
    if not validated:
        raise Exception("Missing {}".format(arg))
