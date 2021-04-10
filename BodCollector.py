from utils import log
logger = log.Logger(Misc)

class NotEnoughItems(Exception):
    pass
    
def fill_bod(bod, item_id):
    logger.info("Trying to fill bod...")
    Journal.Clear()
    Items.UseItem(bod)
    
    while not Journal.Search("The maximum amount of requested items have already been combined to this deed"):
        Gumps.WaitForGump(1526454082, 10000)
        Gumps.SendAction(1526454082, 2)
        Target.WaitForTarget(500, False)
        if not Target.HasTarget():
            continue
        item_to_target = Items.FindByID(item_id, -1, Player.Backpack.Serial)
        if item_to_target is None:
            raise NotEnoughItems()
        Target.TargetExecute(item_to_target)

    Gumps.SendAction(1526454082, 0)    
    logger.info("Bod filled!")



bod = Target.PromptTarget("Select the bulk order deed to fill")
if bod is not None:
    sample_item = Target.PromptTarget("Select a sample item")
    if sample_item is not None:
        target_item_id = Items.FindBySerial(sample_item).ItemID
        try:
            fill_bod(bod, target_item_id)
        except NotEnoughItems:
            Target.Cancel()
            logger.error("Not enough items to fill the bod")
    else:
        logger.error("Sample item is invalid")
    
else:
    logger.error("That is not a valid bod")

    