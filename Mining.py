Journal.Clear()
tile = Target.PromptGroundTarget("Select target to mine.")
while not Journal.Search("There is no metal here to mine."):
    pickaxe = Items.FindByID(3718,-1,Player.Backpack.Serial)
    Items.UseItem(pickaxe.Serial)
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(tile.X, tile.Y, tile.Z)
    Misc.Pause(2000)
Misc.SendMessage("finished mining tile!")