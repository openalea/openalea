


def test_controls():

    from openalea.core.service import create_control
    from openalea.core.control import Control

    print Control('a', value=1,
                  constraints=dict(min=1, max=2))
    print Control('a', 'IInt',
                  constraints=dict(min=3, max=4))
    print Control('a', 'IInt',
                  constraints=dict(min=5, max=6))

    print Control('a', 'IInt')
    print Control('a', value=4)



    print create_control('a', value=1, constraints=dict(min=1, max=2))
    print create_control('a', 'IInt', constraints=dict(min=3, max=4))
    print create_control('a', 'IInt', value=6, constraints=dict(min=5, max=6))
    print create_control('a', 'IInt')
    print create_control('a', value=4)




