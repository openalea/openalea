


def test_controls():

    from openalea.oalab.service import control
    from openalea.oalab.control.control import Control

    print Control('a', value=1,
                  constraints=dict(min=1, max=2))
    print Control('a', 'IInt',
                  constraints=dict(min=3, max=4))
    print Control('a', 'IInt',
                  constraints=dict(min=5, max=6))

    print Control('a', 'IInt')
    print Control('a', value=4)



    print control.create('a', value=1, constraints=dict(min=1, max=2))
    print control.create('a', 'IInt', constraints=dict(min=3, max=4))
    print control.create('a', 'IInt', value=6, constraints=dict(min=5, max=6))
    print control.create('a', 'IInt')
    print control.create('a', value=4)




