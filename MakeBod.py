import re
from utils import log
logger = log.Logger(Misc)

class NotEnoughItems(Exception):
    pass

items_info = {
    # hats
    "skullcap": {
        "gumpId": 2,
        "itemId": 5444,
        "category": 1
    },
    "bandana": {
        "gumpId": 9,
        "itemId": 5440,
        "category": 1
    },
    "floppy hat": {
        "gumpId": 16,
        "itemId": 5907,
        "category": 1
    },
    "cap": {
        "gumpId": 23,
        "itemId": 5909,
        "category": 1
    },
    "wide-brim hat": {
        "gumpId": 30,
        "itemId": 5908,
        "category": 1
    },
    "straw hat": {
        "gumpId": 37,
        "itemId": 5911,
        "category": 1
    },
    "tall straw hat": {
        "gumpId": 44,
        "itemId": 5910,
        "category": 1
    },
    "wizard's hat": {
        "gumpId": 51,
        "itemId": 5912,
        "category": 1
    },
    "bonnet": {
        "gumpId": 58,
        "itemId": 5913,
        "category": 1
    },
    "feathered hat": {
        "gumpId": 65,
        "itemId": 5914,
        "category": 1
    },
    "tricorne hat": {
        "gumpId": 72,
        "itemId": 5915,
        "category": 1
    },
    "jester hat": {
        "gumpId": 79,
        "itemId": 5916,
        "category": 1
    },
    "flower garland": {
        "gumpId": 86,
        "itemId": 8966,
        "category": 1
    },

    # shirts
    "doublet": {
        "gumpId": 2,
        "itemId": 8059,
        "category": 8
    },
    "shirt": {
        "gumpId": 9,
        "itemId": 5399,
        "category": 8
    },
    "fancy shirt": {
        "gumpId": 16,
        "itemId": 7933,
        "category": 8
    },
    "tunic": {
        "gumpId": 23,
        "itemId": 8097,
        "category": 8
    },
    "surcoat": {
        "gumpId": 30,
        "itemId": 8189,
        "category": 8
    },
    "plain dress": {
        "gumpId": 37,
        "itemId": 7937,
        "category": 8
    },
    "fancy dress": {
        "gumpId": 44,
        "itemId": 7936,
        "category": 8
    },
    "cloak": {
        "gumpId": 51,
        "itemId": 5397,
        "category": 8
    },
    "robe": {
        "gumpId": 58,
        "itemId": 7939,
        "category": 8
    },
    "jester suit": {
        "gumpId": 65,
        "itemId": 8095,
        "category": 8
    },
    
    # pants
    "short pants": {
        "gumpId": 2,
        "itemId": 5422,
        "category": 15
    },
    "long pants": {
        "gumpId": 9,
        "itemId": 5433,
        "category": 15
    },
    "kilt": {
        "gumpId": 16,
        "itemId": 5431,
        "category": 15
    },
    "skirt": {
        "gumpId": 23,
        "itemId": 5398,
        "category": 15
    },

    # miscellaneous
    "body sash": {
        "gumpId": 2,
        "itemId": 5441,
        "category": 22
    },
    "half apron": {
        "gumpId": 9,
        "itemId": 5435,
        "category": 22
    },
    "full apron": {
        "gumpId": 16,
        "itemId": 5437,
        "category": 22
    },
    
    # footwear
    "sandals": {
        "gumpId": 30,
        "itemId": 5901,
        "category": 29
    },
    "shoes": {
        "gumpId": 37,
        "itemId": 5903,
        "category": 29
    },
    "boots": {
        "gumpId": 44,
        "itemId": 5899,
        "category": 29
    },
    "thigh boots": {
        "gumpId": 51,
        "itemId": 5905,
        "category": 29
    },
    
    # leather armor
    "leather gorget": {
        "gumpId": 23,
        "itemId": 5063,
        "category": 36
    },
    "leather cap": {
        "gumpId": 30,
        "itemId": 7609,
        "category": 36
    },
    "leather gloves": {
        "gumpId": 37,
        "itemId": 5062,
        "category": 36
    },
    "leather sleeves": {
        "gumpId": 44,
        "itemId": 5069,
        "category": 36
    },
    "leather leggings": {
        "gumpId": 51,
        "itemId": 5067,
        "category": 36
    },
    "leather tunic": {
        "gumpId": 58,
        "itemId": 5068,
        "category": 36
    },
    
    # female armor
    "leather shorts": {
        "gumpId": 2,
        "itemId": 7168,
        "category": 50
    },
    "leather skirt": {
        "gumpId": 9,
        "itemId": 7176,
        "category": 50
    },
    "leather bustier": {
        "gumpId": 16,
        "itemId": 7178,
        "category": 50
    },
    "studded bustier": {
        "gumpId": 23,
        "itemId": 7180,
        "category": 50
    },
    "female leather armor": {
        "gumpId": 30,
        "itemId": 7174,
        "category": 50
    },
    "studded armor": {
        "gumpId": 37,
        "itemId": 7170,
        "category": 50
    },
    
    # studded armor
    "studded gorget": {
        "gumpId": 2,
        "itemId": 5078,
        "category": 43
    },
    "studded gloves": {
        "gumpId": 9,
        "itemId": 5068,
        "category": 43
    },
    "studded sleeves": {
        "gumpId": 16,
        "itemId": 5068,
        "category": 43
    },
    "studded leggings": {
        "gumpId": 23,
        "itemId": 5082,
        "category": 43
    },
    "studded tunic": {
        "gumpId": 30,
        "itemId": 5083,
        "category": 43
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
        result = re.search('^([a-z A-Z\`\´\'\-]+): ([0-9]+)$', item_type_prop)
        return result.group(1)
        
    def amount_done(self):
        item_type_prop = self._item_type_prop()
        result = re.search('^([a-z A-Z\`\´\'\-]+): ([0-9]+)$', item_type_prop)
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
        
    def use(self):
        Items.UseItem(self.item)
        
    
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
    tailor_craft_gump.press_button(item_info["category"])
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

        
def try_fill_bod_with_item(bod, item_id):
    logger.info("Trying to fill bod...")
    Journal.Clear()
    
    bod.use()
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


def fill_bod(bod):
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
            try_fill_bod_with_item(bod, item_info["itemId"])
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
    bod = BulkOrderDeed(bod_item)
    fill_bod(bod)
    
8792
        