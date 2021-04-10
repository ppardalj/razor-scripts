import re
from utils import log
logger = log.Logger(Misc)

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
        result = re.search('^([a-z A-Z]+): ([0-9]+)$', item_type_prop)
        return result.group(1)
        
    def amount_done(self):
        item_type_prop = self._item_type_prop()
        result = re.search('^([a-z A-Z]+): ([0-9]+)$', item_type_prop)
        return int(result.group(2))
        
    def _item_type_prop(self):
        props = Items.GetPropStringList(self.item)
        item_type_prop = props[props.Count - 1]
        return item_type_prop
    
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

def make_item(item_info):
    sewing_kit = find_sewing_kit()
    Items.UseItem(sewing_kit)
    tailor_craft_gump = TailorCraftGump()
    tailor_craft_gump.wait_for()
    tailor_craft_gump.press_button(item_info["gumpId"])
    tailor_craft_gump.wait_for()
    tailor_craft_gump.close()
    Misc.Pause(500)
        
def fill_bod():
    item = Target.PromptTarget("Select the bulk order deed to fill")
    if item is None:
        logger.error("That is not a valid bod")
        return
       
    bod = BulkOrderDeed(item)
    
    item_name = bod.item_name()
    amount_to_make = bod.amount_to_make()
    amount_done = bod.amount_done()
    
    Misc.SendMessage("Item name: " + item_name)
    Misc.SendMessage("Amount to make: " + str(amount_to_make))
    Misc.SendMessage("Amount done: " + str(amount_done))
    
    item_info = items_info[item_name]
    logger.info(str(item_info["gumpId"]))
    logger.info(str(item_info["itemId"]))

    logger.info("Bod progress: " + str(amount_done) + "/" + str(amount_to_make))

    while amount_done < amount_to_make:
        logger.info("Will make another item")
        make_item(item_info)
        amount_done += 1
        logger.info("Bod progress: " + str(amount_done) + "/" + str(amount_to_make))
        
    if amount_done >= amount_to_make:
        logger.info("Finished making goods!")
    else:
        logger.error("Something went wrong")
 
fill_bod()
        