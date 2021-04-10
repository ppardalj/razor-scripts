class CPlayer:
    def find_item_in_backpack(self, item_id):
        return Items.FindByID(item_id, -1, Player.Backpack.Serial)

player = CPlayer()
bulk_order_book = player.find_item_in_backpack(0x2259)
if bulk_order_book is not None:
    Misc.SendMessage(bulk_order_book.Name)
else:
    Misc.SendMessage("Could not find bulk order book in backpack")

Items.UseItem(bulk_order_book)
Items.UseItem(0x41F472DD) # bulk order book
Gumps.WaitForGump(1425364447, 10000)
Gumps.SendAction(1425364447, 0)