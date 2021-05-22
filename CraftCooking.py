def use_skillet():
    skillet = Items.FindByID(2431, -1, Player.Backpack.Serial)
    if skillet is None:
        raise Exception("Error: could not find skillet")
    Items.UseItem(skillet.Serial)


def make_last():
    use_skillet()
    Gumps.WaitForGump(949095101, 10000)
    Misc.Pause(500)
    Gumps.SendAction(949095101, 21)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 0)
    Misc.Pause(500)

while True:
    make_last()
