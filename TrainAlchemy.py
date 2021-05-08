while True:
    pen = Items.FindByID(3739,-1,Player.Backpack.Serial)
    Items.UseItem(pen.Serial)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 21)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 0)
    Misc.Pause(500)