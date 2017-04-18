import tables
from shutil import copyfile


def remove_configs(filename, cluster, stationnumber):
    """
    Remove all but the first configuration row
    """
    
    copyfile(filename, filename+'_backup')

    with tables.open_file(filename, "a") as data:
        config = data.get_node("/hisparc/cluster_"+cluster+"/station_"+str(stationnumber)+"/config")
        print len(config)
        config.remove_rows(1,len(config))



if __name__ == "__main__":
    remove_configs("2017_4_15.h5", "amsterdam", 4)
