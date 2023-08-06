def dict_get_path(data, *path, default=None):
    return dict_get_path(data.get(path[0], default), *path[1:]) if path and data else data