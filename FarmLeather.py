from utils import log
from System.Collections.Generic import List
logger = log.Logger(Misc)

def find_corpses():
    corpse_filter = Items.Filter()
    corpse_filter.Movable = False
    corpse_filter.RangeMax = 2
    corpse_filter.Graphics = List[int]([0x2006])
    corpses = Items.ApplyFilter(corpse_filter)
    return corpses


def find_scissors():
    return Items.FindByID(3999,-1,Player.Backpack.Serial)


def find_dagger():
    return Items.FindByID(3922,-1,Player.Backpack.Serial)


def carve_corpse(corpse):
    Journal.Clear()
    dagger = find_dagger()
    while not Journal.Search("What do you want to use this item on?"):
        Misc.Pause(500)
        Items.UseItem(dagger)
        Target.WaitForTarget(500, False)
        Target.TargetExecute(corpse)


def cut_item(item):
    Misc.Pause(500)
    scissors = find_scissors()
    Items.UseItem(scissors)
    Target.WaitForTarget(500, False)
    Misc.Pause(500)
    Target.TargetExecute(item)

def move_to_backpack(ribs):
    Misc.Pause(500)
    Items.Move(ribs, Player.Backpack, ribs.Amount)

def farm_corpse(corpse):
    ribs = Items.FindByID(2545, -1, corpse.Serial)
    if ribs is not None:
        logger.info('Found ribs -> move to backpack')
        move_to_backpack(ribs)
    leather = Items.FindByID(4217, -1, corpse.Serial)
    if leather is not None:
        logger.info('Found leather -> move to backpack and cut')
        move_to_backpack(leather)


def farm_leather():
    carved_corpses = set()
    farmed_corpses = set()
    while True:
        # find leather
        leather = Items.FindByID(4217, -1, Player.Backpack.Serial)
        if leather is not None:
            Misc.Pause(500)
            cut_item(leather)
            continue

        # find corpses
        corpses = find_corpses()
        for corpse in corpses:
            if corpse.Serial not in carved_corpses: # not carved yet
                logger.info('Found uncarved corpse -> carving')
                Misc.Pause(500)
                carve_corpse(corpse)
                carved_corpses.add(corpse.Serial)
                continue
            elif corpse.Serial not in farmed_corpses:
                logger.info('Found carved corpse -> farming')
                farm_corpse(corpse)
                farmed_corpses.add(corpse.Serial)
                continue

        Misc.Pause(1000)
        logger.info('Idling...')

farm_leather()