r"""
>>> from workflow.flow.cclock.lock.clearlock import add_master
>>> vobbranch = '10G_CHT_06MAR30_BR@\NetRing'
>>> users = 'hz08678,hz08483'
>>> print add_master(vobbranch,users)
hz08678,hz08483,hz15018,hz20018,hz05172
>>> users = ''
>>> print add_master(vobbranch,users)
hz15018,hz20018,hz05172
>>> vobbranch = '10G_CHT_06MAR30_BR@\NetRing___'
>>> users = 'hz08678,hz08483'
>>> print add_master(vobbranch,users)
hz08678,hz08483
"""
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '../..')
    import doctest
    doctest.testmod() 
