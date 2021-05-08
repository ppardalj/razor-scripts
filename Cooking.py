container = 1142886297

def find_raw_ribs_in_backpack():
    return Items.FindByID(2545,-1,Player.Backpack.Serial)


def get_some_raw_ribs():
    raw_ribs = Items.FindByID(2545,-1,container)

    if raw_ribs is None:
        Misc.SendMessage("Error: could not find raw ribs")
    else:
        Misc.SendMessage("Moving some ribs from container")
        Items.Move(raw_ribs,Player.Backpack.Serial,1)
        Misc.Pause(1000)

    
def use_skillet():
    skillet = Items.FindByID(2431,-1,Player.Backpack.Serial)

    if skillet is None:
        raise Exception("Error: could not find skillet")
    
    Items.UseItem(skillet.Serial)
        
def craft_ribs():
    Misc.SendMessage("Crafting ribs")
    use_skillet()    
    Gumps.WaitForGump(949095101, 10000)
    Misc.Pause(500)
    Gumps.SendAction(949095101, 21)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 0)
    Misc.Pause(500)
    
def train_cooking():
    while True:
        raw_ribs = find_raw_ribs_in_backpack()
        if raw_ribs is None:
            get_some_raw_ribs()
            raw_ribs = find_raw_ribs_in_backpack()
        craft_ribs()
        
train_cooking()