from gaming import gameobj


class MyGameObj(gameobj.GameObject):
    pass


class MySubGameObj(MyGameObj):
    pass


class MyOtherGameObj(gameobj.GameObject):
    pass


def test_gameobjmeta():

    class Class1(metaclass=gameobj.GameObjMeta):
        pass

    assert Class1._logname is None
    assert Class1._loglvl == "INFO"
    assert Class1._logpath is None

    class Class11(Class1):
        pass

    # Make sure class attributes are not bounded
    Class1._loglvl += "_broke"
    assert Class1._loglvl == "INFO_broke"
    assert Class11._loglvl == "INFO"


def test_gameobject():

    gameobj.GameObject.reset_counter()

    # ----------------------------------------------------------------------- #
    # Creation and counting

    instance = gameobj.GameObject()
    assert instance.name == "GameObject_1"
    assert instance.get_loglvl() == 20

    instance = gameobj.GameObject(
        identity="new",
        loglvl=10,
    )
    assert instance.name == "GameObject_new"
    assert instance.get_loglvl() == 10

    instance = gameobj.GameObject()
    assert instance.name == "GameObject_3"

    instance = MyGameObj(
        identity="first"
    )
    assert instance.name == "MyGameObj_first"

    instance = MyGameObj()
    assert instance.name == "MyGameObj_2"

    instance = MySubGameObj()
    assert instance.name == "MySubGameObj_1"

    instance = MyOtherGameObj()
    assert instance.name == "MyOtherGameObj_1"

    assert gameobj.GameObject.counter == {
        gameobj.GameObject: 7,
        MyGameObj: 3,
        MyOtherGameObj: 1,
        MySubGameObj: 1,
    }

    # ----------------------------------------------------------------------- #
    # Params

    dft_params = {
        'identity': None,
        'name': None,
        'loglvl': "INFO",
        'logpath': None,
    }

    assert gameobj.GameObject.dft_params() == dft_params
    assert MyGameObj.dft_params() == dft_params
    assert MySubGameObj.dft_params() == dft_params

    gameobj.GameObject.set_dft_loglvl("DEBUG", propag=True)
    MyGameObj.set_dft_loglvl("ERROR")

    assert gameobj.GameObject.dft_params()['loglvl'] == "DEBUG"
    assert MyGameObj.dft_params()['loglvl'] == "ERROR"
    assert MySubGameObj.dft_params()['loglvl'] == "DEBUG"

    base = gameobj.GameObject()
    instance = MyGameObj()
    subinstance = MySubGameObj()

    assert base.get_loglvl(explicit=True) == "DEBUG"
    assert instance.get_loglvl(explicit=True) == "ERROR"
    assert subinstance.get_loglvl(explicit=True) == "DEBUG"
