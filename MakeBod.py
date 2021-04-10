import re

def log_info(message):
    Misc.SendMessage("INFO: " + message)
    
def log_error(message):
    Misc.SendMessage("ERROR: " + message)

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
        
    def close(self):
        Gumps.SendAction(self.gump_id, 0)
        
def fill_bod():
    item = Target.PromptTarget("Select the bulk order deed to fill")
    if item is not None:
        bod = BulkOrderDeed(item)
        
        item_name = bod.item_name()
        amount_to_make = bod.amount_to_make()
        amount_done = bod.amount_done()
        
        Misc.SendMessage("Item type: " + item_name)
        Misc.SendMessage("Amount to make: " + str(amount_to_make))
        Misc.SendMessage("Amount done: " + str(amount_done))
        
        tailor_craft_gump = TailorCraftGump()
        
        sewing_kit = find_sewing_kit()
        Items.UseItem(sewing_kit)
        
        tailor_craft_gump.wait_for()
        
        Misc.SendMessage("Please craft the first item")
        Misc.Pause(10000)
        amount_done += 1
        log_info("Bod progress: " + str(amount_done) + "/" + str(amount_to_make))
        
        while amount_done < amount_to_make:
            log_info("Will make another item")
            tailor_craft_gump.wait_for()
            tailor_craft_gump.make_last()
            amount_done += 1
            tailor_craft_gump.wait_for()
            log_info("Bod progress: " + str(amount_done) + "/" + str(amount_to_make))
            
        if amount_done >= amount_to_make:
            log_info("Finished making goods!")
            tailor_craft_gump.close()
        else:
            log_error("Something went wrong")
    else:
        log_error("That is not a valid bod")
 
fill_bod()       
#fill_bod()

    
        