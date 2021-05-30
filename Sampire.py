from utils import log
logger = log.Logger(Misc)

while True:
    if not Player.BuffsExist('Lightning Strike'):
        Spells.CastBushido('Lightning Strike')
        Misc.Pause(300)
        continue
    if not Player.BuffsExist('Curse Weapon'):
        scroll = Items.FindByID(8803, -1, Player.Backpack.Serial)
        Items.UseItem(scroll)
        Misc.Pause(2000)
        continue
    if not Player.BuffsExist('Enemy Of One'):
        Spells.CastChivalry('Enemy Of One')
        Misc.Pause(2000)
        continue
    if not Player.BuffsExist('Divine Fury'):
        Spells.CastChivalry('Divine Fury')
        Misc.Pause(2000)
        continue
    if not Player.BuffsExist('Consecrate Weapon'):
        Spells.CastChivalry('Consecrate Weapon')
        Misc.Pause(2000)
        continue
    logger.info('no cast needed')
    Misc.Pause(1000)
