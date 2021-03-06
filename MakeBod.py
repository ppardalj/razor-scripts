import re
from utils import log
from data import tailoring
logger = log.Logger(Misc)

class NotEnoughItems(Exception):
    pass

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

    def is_small(self):
        props = Items.GetPropStringList(self.item)
        for prop in props:
            if prop.find("small") != -1:
                return True
            if prop.find("large") != -1:
                return False
        return False

    def move_to(self, to):
        Items.Move(self.item, to, 1)
        Misc.Pause(500)

    def is_exceptional(self):
        props = Items.GetPropStringList(self.item)
        for prop in props:
            if prop.find("exceptional") != -1:
                return True
        return False

def print_item_id():
    item_serial = Target.PromptTarget("Target the item")
    item_id = Items.FindBySerial(item_serial).ItemID
    Misc.SendMessage(item_id)
    
class ToolNotFound(Exception):
    pass

def find_scissors():
    return Items.FindByID(3999, -1, Player.Backpack.Serial)

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
    sewing_kit = find_sewing_kit()
    Items.UseItem(sewing_kit)
    Misc.Pause(500)
    tailor_craft_gump = TailorCraftGump()
    tailor_craft_gump.wait_for()
    tailor_craft_gump.press_button(item_info["category"])
    tailor_craft_gump.wait_for()
    tailor_craft_gump.press_button(item_info["gumpId"])
    tailor_craft_gump.wait_for()
    Misc.Pause(1000)
    tailor_craft_gump.close()

def combine_bod_with_item(bod, item_to_target):
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
    Target.TargetExecute(item_to_target)
    Misc.Pause(500)

def is_item_exceptional(item):
    props = Items.GetPropStringList(item)
    for prop in props:
        if prop.find("exceptional") != -1:
            return True
    return False

def fill_bod(bod):
    bod.dump_info()
    
    item_name = bod.item_name()
    item_info = tailoring.items_info[item_name]
    item_id = item_info["itemId"]
    logger.info(str(item_info["gumpId"]))
    logger.info(str(item_id))

    bod.show_progress()
    while not bod.is_complete():
        item_to_target = Items.FindByID(item_id, -1, Player.Backpack.Serial)
        while item_to_target is None:
            logger.info("Not enough items to fill the bod -> will make another item")
            make_item(item_info)
            Misc.Pause(500)
            item_to_target = Items.FindByID(item_id, -1, Player.Backpack.Serial)
        if bod.is_exceptional() and not is_item_exceptional(item_to_target):
            logger.info("Required exceptional item, but crafted normal -> cutting item")
            cut_item(item_to_target)
        else:
            logger.info("Item done! -> combining with deed")
            combine_bod_with_item(bod, item_to_target)
        bod.show_progress()
        Misc.Pause(1000)

    if bod.is_complete():
        logger.info("Bod is complete!")
    else:
        logger.error("Something went wrong")

def cut_item(item_to_target):
    scissors = find_scissors()
    Items.UseItem(scissors)
    Target.WaitForTarget(500, False)
    Misc.Pause(500)
    Target.TargetExecute(item_to_target)

def target_bod_to_fill():
    bod_item = Target.PromptTarget("Select the bulk order deed to fill")
    if bod_item is None:
        logger.error("That is not a valid bod")
    else:
        bod = BulkOrderDeed(bod_item)
        fill_bod(bod)

def find_bod():
    return Items.FindByID(8792, -1, Player.Backpack.Serial)

def fill_all_bods_in_backpack():
    book = Items.FindBySerial(1227041137)
    bod_item = find_bod()
    while bod_item is not None:
        bod = BulkOrderDeed(bod_item)
        if bod.is_small():
            logger.info("Found a small bod -> filling")
            fill_bod(bod)
        else:
            logger.info("Found a large bod -> moving to book")
        bod.move_to(book)
        bod_item = find_bod()
    logger.info("No more bods to fill")

fill_all_bods_in_backpack()
        