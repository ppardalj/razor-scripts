from utils import log
from System.Collections.Generic import List
logger = log.Logger(Misc)

def find_corpse():
    corpse_filter = Items.Filter()
    corpse_filter.Movable = False
    corpse_filter.RangeMax = 2
    corpse_filter.Graphics = List[int]([0x2006])
    corpses = Items.ApplyFilter(corpse_filter)
    for corpse in corpses:
        return corpse
    return None


def find_scissors():
    return Items.FindByID(3999,-1,Player.Backpack.Serial)


def find_dagger():
    return Items.FindByID(3922,-1,Player.Backpack.Serial)


def carve_corpse(corpse):
    dagger = find_dagger()
    Items.UseItem(dagger)
    Target.WaitForTarget(500, False)
    Misc.Pause(500)
    Target.TargetExecute(corpse)
    Misc.Pause(500)


def cut_item(item):
    scissors = find_scissors()
    Items.UseItem(scissors)
    Target.WaitForTarget(500, False)
    Misc.Pause(500)
    Target.TargetExecute(item)
    Misc.Pause(500)

def move_to_backpack(ribs):
    Items.Move(ribs, Player.Backpack, ribs.Amount)
    Misc.Pause(1000)

def farm_corpse(corpse):
    carve_corpse(corpse)
    ribs = Items.FindByID(2545, -1, corpse.Serial)
    if ribs is not None:
        logger.info('Found ribs -> move to backpack')
        move_to_backpack(ribs)
    leather = Items.FindByID(4217, -1, corpse.Serial)
    if leather is not None:
        logger.info('Found leather -> move to backpack and cut')
        move_to_backpack(leather)
        cut_item(leather)

def farm_leather():
    carved_corpses = set()
    while True:
        corpse = find_corpse()
        if corpse is not None and corpse.Serial not in carved_corpses:
            logger.info('Found corpse -> carving')
            Misc.Pause(1000) # just in case we were doing sth else
            farm_corpse(corpse)
            carved_corpses.add(corpse.Serial)
        else:
            logger.info('Corpse not found')
        Misc.Pause(1000)

farm_leather()