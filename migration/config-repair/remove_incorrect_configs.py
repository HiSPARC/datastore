import tables


def remove_configs(filename, cluster, stationnumber):
    """
    Remove all but the first configuration row for a given cluster and stationnumber
    """

    with tables.open_file(filename, 'a') as data:
        config = data.get_node(f'/hisparc/cluster_{cluster}/station_{stationnumber}/config')
        config.remove_rows(1)


if __name__ == '__main__':
    remove_configs('2017_4_15.h5', 'amsterdam', 4)
