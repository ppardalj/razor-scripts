import re
from utils import log
logger = log.Logger(Misc)

class NotEnoughItems(Exception):
    pass

items_info = {
    "skullcap": {
        "gumpId": 2,
        "itemId": 5444
    },
    "bandana": {
        "gumpId": 9,
        "itemId": 5440 
    },
    "floppy hat": {
        "gumpId": 16,
        "itemId": 5907
    },
    "cap": {
        "gumpId": 23,
        "itemId": 5909
    },
    "wide-brim hat": {
        "gumpId": 30,
        "itemId": 5908
    },
    "straw hat": {
        "gumpId": 37,
        "itemId": 5911
    },
    "tall straw hat": {
        "gumpId": 44,
        "itemId": 5910
    },
    "wizard's hat": {
        "gumpId": 51,
        "itemId": 5912
    },
    "bonnet": {
        "gumpId": 58,
        "itemId": 5913
    },
    "feathered hat": {
        "gumpId": 65,
        "itemId": 5914
    },
    "tricorne hat": {
        "gumpId": 72,
        "itemId": 5915
    },
    "jester hat": {
        "gumpId": 79,
        "itemId": 5916
    },
    "flower garland": {
        "gumpId": 86,
        "itemId": 8966
    }
}

class BulkOrderDeed:
    def __init__(self, item):
        Items.WaitForProps(item, 1000)
        self.item = item
        
    def amount_to_make(self):
        return int(Items.GetPropValue(self.item, "amount to make").ToString())
        
    def item_name(self):
        props = Items.GetPropStringList(self.item)
        item_type_prop = props[props.Count - 1]
        result = re.search('^([a-z A-Z\`\´\']+): ([0-9]+)$', item_type_prop)
        return result.group(1)
        
    def amount_done(self):
        item_type_prop = self._item_type_prop()
        result = re.search('^([a-z A-Z\`\´\']+): ([0-9]+)$', item_type_prop)
        return int(result.group(2))
        
    def _item_type_prop(self):
        props = Items.GetPropStringList(self.item)
        item_type_prop = props[props.Count - 1]
        return item_type_prop

    def dump_info(self):
        Misc.SendMessage("Item name: " + self.item_name())
        Misc.SendMessage("Amount to make: " + str(self.amount_to_make()))
        Misc.SendMessage("Amount done: " + str(self.amount_done()))
        
    def is_complete(self):
        return self.amount_done() >= self.amount_to_make()
        
    def show_progress(self):
        logger.info("Bod progress: " + str(self.amount_done()) + "/" + str(self.amount_to_make()))
        
    
def print_item_id():
    item_serial = Target.PromptTarget("Target the item")
    item_id = Items.FindBySerial(item_serial).ItemID
    Misc.SendMessage(item_id)
    
class ToolNotFound(Exception):
    pass
    
def find_sewing_kit():
    tool_serial = Items.FindByID(3997, -1, Player.Backpack.Serial)
    if tool_serial is None:
        raise ToolNotFound()
    return tool_serial

class TailorCraftGump:
    def __init__(self):
        self.gump_id = 949095101
    
    def wait_for(self):
        Gumps.WaitForGump(self.gump_id, 10000)
        
    def make_last(self):
        Gumps.SendAction(self.gump_id, 21)
        
    def press_button(self, button_id):
        Gumps.SendAction(self.gump_id, button_id)
        
    def close(self):
        Gumps.SendAction(self.gump_id, 0)

class BodGump:
    def __init__(self):
        self.gump_id = 1526454082
    
    def wait_for(self):
        Gumps.WaitForGump(self.gump_id, 10000)
        
    def combine(self):
        Gumps.SendAction(self.gump_id, 2)
        
    def close(self):
        Gumps.SendAction(self.gump_id, 0)
        
def make_item(item_info):
    logger.info("Trying to make item")
    sewing_kit = find_sewing_kit()
    Items.UseItem(sewing_kit)
    Misc.Pause(500)
    logger.info("Using tool")
    tailor_craft_gump = TailorCraftGump()
    tailor_craft_gump.wait_for()
    tailor_craft_gump.press_button(item_info["gumpId"])
    tailor_craft_gump.wait_for()
    Misc.Pause(1000)
    tailor_craft_gump.close()
    logger.info("Item done")
        
def make_bod():
    item = Target.PromptTarget("Select the bulk order deed to fill")
    if item is None:
        logger.error("That is not a valid bod")
        return
       
    bod = BulkOrderDeed(item)
    
    item_name = bod.item_name()
    amount_to_make = bod.amount_to_make()
    amount_done = bod.amount_done()
    
    bod.dump_info()
    
    item_info = items_info[item_name]
    logger.info(str(item_info["gumpId"]))
    logger.info(str(item_info["itemId"]))

    bod.show_progress()

    while not bod.is_complete():
        logger.info("Will make another item")
        make_item(item_info)
        amount_done += 1
        bod.show_progress()
        
    if amount_done >= amount_to_make:
        logger.info("Finished making goods!")
    else:
        logger.error("Something went wrong")

        
def try_fill_bod_with_item(bod_item, item_id):
    logger.info("Trying to fill bod...")
    Journal.Clear()
    
    Items.UseItem(bod_item)
    Misc.Pause(500)
    bod_gump = BodGump()
    bod_gump.wait_for()
    bod_gump.combine()
    bod_gump.wait_for()
    bod_gump.close()
    Target.WaitForTarget(500, False)
    if not Target.HasTarget():
        if not Journal.Search("The maximum amount of requested items have already been combined to this deed"):
            raise Exception("Target was not prompted, but bod is not complete. What happened?")
    item_to_target = Items.FindByID(item_id, -1, Player.Backpack.Serial)
    if item_to_target is None:
        Misc.Pause(500)
        raise NotEnoughItems()
    Target.TargetExecute(item_to_target)
    Misc.Pause(500)
    logger.info("Added 1 item to bod!")


def fill_bod(bod_item):
    bod = BulkOrderDeed(bod_item)
    bod.dump_info()
    
    item_name = bod.item_name()
    amount_to_make = bod.amount_to_make()
    amount_done = bod.amount_done()
    
    item_info = items_info[item_name]
    logger.info(str(item_info["gumpId"]))
    logger.info(str(item_info["itemId"]))

    bod.show_progress()
    
    while not bod.is_complete():
        # First look if there is an item already crafter
        try:
            try_fill_bod_with_item(bod_item, item_info["itemId"])
            bod.show_progress()
        except NotEnoughItems:
            Target.Cancel()
            logger.info("Not enough items to fill the bod. Will make another item")
            make_item(item_info)

    if bod.is_complete():
        logger.info("Bod is complete!")
    else:
        logger.error("Something went wrong")

bod_item = Target.PromptTarget("Select the bulk order deed to fill")
if bod_item is None:
    logger.error("That is not a valid bod")
else:
    fill_bod(bod_item)
        