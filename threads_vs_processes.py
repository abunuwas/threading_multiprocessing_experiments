
if __name__ == "__main__":

    import timeit

    process_time = timeit.timeit('run_processes()',
                                 setup='from processes import run_processes',
                                 number=1)
    threading_time = timeit.timeit('run_threads()',
                                   setup="from threads import run_threads",
                                   number=1)

    print("""
    Time to analyze texts with threads: {}
    Time to analyze texts with multiprocessing: {}
    """.format(threading_time, process_time))
