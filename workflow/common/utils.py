# -*- coding: UTF-8 -*-
def pickle_obj(filename, data):
    """
    pickle对象到指定文件
    """
    output = open(filename, 'wb')
    import pickle
    pickle.dump(data, output)
    output.close()

def load_pickle_obj(filename):
    pkl_file = open(filename, 'rb')
    import pickle
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data
