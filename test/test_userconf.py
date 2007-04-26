# Test user configuration

from openalea.core.session import UserConfig


# [PackageManager]

# path = ['.']
# userpath = '~/.openalea/wralea'


# [DataflowEditor]

# doubleclick = ["open", "run"]


def test_config():

    session = Session()
    
    session.config
    
