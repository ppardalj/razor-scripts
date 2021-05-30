from utils import log
logger = log.Logger(Misc)

while True:
    if not Player.BuffsExist('Enemy Of One'):
        logger.info('Should cast Enemy Of One')
    if not Player.BuffsExist('Consecrate Weapon'):
        logger.info('Should cast Consecrate Weapon')
    if not Player.BuffsExist('Wraith Form'):
        logger.info('Should cast Wraith Form')
    if not Player.BuffsExist('Divine Fury'):
        logger.info('Should cast Divine Fury')
    if not Player.BuffsExist('Curse Weapon'):
        logger.info('Should cast Curse Weapon')

    Misc.Pause(1000)
