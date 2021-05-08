
while True:
    pen = Items.FindByID(4031,-1,Player.Backpack.Serial)
    Items.UseItem(pen.Serial)
    Gumps.WaitForGump(949095101, 10000)
    Misc.Pause(500)
    Gumps.SendAction(949095101, 21)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 0)
    Misc.Pause(500)