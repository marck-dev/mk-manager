from pathlib import Path
import json

def get_conf_file():
    home = Path.home().absolute() 
    CONFILE_URLS = [
        "{}/.mk-manager.conf".format(home),
        "/etc/mk-d-manager/manager.conf"
    ]
    conf_id = False
    for i, path in enumerate(CONFILE_URLS):
        if Path(path).exists():
            conf_id = path
            break
    if not conf_id == False:
        file = open(conf_id, 'r', encoding="utf-8")
        data = file.readlines()
        data = "\n".join(data)
        file.close()
        confs = json.loads(data)
        return confs,conf_id
    else:
        print("\033[0;31mNot found config file!\033[0m")
        return []
    
    
def load_config():
    from display_gui import build_command
    confs,_ = get_conf_file()
    for conf in confs:
        build_command(**conf)
    

def save_config(target, auto=True, 
                  base=False,
                  position=False,
                  primary=False,
                  rotate=False):
    
    confs,file = get_conf_file()
    # search for the target
    target_id = None
    for i,conf in enumerate(confs):
        if conf['target']['port'] == target['port']:
            target_id = i
            break
    if target_id is not None:
        conf = confs[target_id]
        if base:
            if conf['base']['port'] != base['port']:
                conf['base'] = base
            conf['position'] = position
            conf['rotate'] = rotate
    else:
        data = {
            'target': target,
            'base': base,
            'rotate': rotate,
            'primary': primary,
            'auto': auto,
            'position':position
            }
        confs.append(data)
        str_data = json.dumps(confs, indent=2)
        f = open(file, 'w')
        f.writelines(str_data)
        f.write('\n');
        f.close()