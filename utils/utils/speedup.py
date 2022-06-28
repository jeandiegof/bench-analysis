def calculate_speedups(dataframe):
    """Takes a dataframe containing the columns threads, name, branch and wall_clock_time_us
    and returns a dictionary containg the speedup of each triple (name, cores, branch)"""
    
    single_core_df = dataframe[dataframe['threads'] == 1]
    multi_core_df = dataframe[dataframe['threads'] > 1]
    speedups = {'name': [], 'speedup': [], 'cores': [], 'branch': []}

    for algorithm in set(dataframe['name']):
        single_core_mean = 18446744073709551615

        for branch in set(dataframe['branch']):
            algorithm_single_core_branch = single_core_df[(single_core_df['name'] == algorithm) &
                                                          (single_core_df['branch'] == branch)]
            
            branch_mean = algorithm_single_core_branch['wall_clock_time_us'].mean()
            single_core_mean = min(single_core_mean, branch_mean)
            
        for branch in set(dataframe['branch']):
            for thread in set(multi_core_df['threads']):
                algorithm_multi_core_df = multi_core_df[(multi_core_df['name'] == algorithm) &
                                                        (multi_core_df['threads'] == thread) &
                                                        (multi_core_df['branch'] == branch)]

                multi_core_mean = algorithm_multi_core_df['wall_clock_time_us'].mean()
                speedup = single_core_mean / multi_core_mean

                speedups['name'].append(algorithm)
                speedups['speedup'].append(speedup)
                speedups['cores'].append(thread)
                speedups['branch'].append(branch)
    
    return speedups
