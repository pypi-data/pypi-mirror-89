#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Synchronize Pipes' data with sources

NOTE: `sync` required a SQL connection and is not intended for client use
"""

def sync(
        action : list = [''],
        **kw        
    ) -> tuple:
    """
    Sync elements
    """
    from meerschaum.utils.misc import choose_subaction
    options = {
        'pipes'   : _sync_pipes,
    }
    return choose_subaction(action, options, **kw)

def _pipes_lap(
        workers : int = None,
        debug : bool = None,
        unblock : bool = False,
        force : bool = False,
        min_seconds : int = 1,
        **kw
    ) -> tuple:
    """
    Do a lap of syncing Pipes
    """
    from meerschaum import get_pipes
    from meerschaum.utils.debug import dprint
    from meerschaum.utils.misc import enforce_gevent_monkey_patch, attempt_import
    from meerschaum.utils.formatting import print_tuple
    import time
    pipes = get_pipes(
        as_list = True,
        method = 'registered',
        debug = debug,
        **kw
    )

    def sync_pipe(p):
        """
        Wrapper function for the Pool
        """
        from meerschaum.utils.warnings import warn
        try:
            ### NOTE: skip check_existing flag
            return_tuple = p.sync(
                blocking = (not unblock),
                force = force,
                debug = debug,
                min_seconds = min_seconds,
                workers = workers
            )
        except Exception as e:
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)
            print("Error: " + str(e))
            return_tuple = (False, f"Failed to sync Pipe '{p}' with exception:" + "\n" + str(e))
        
        print_tuple(return_tuple)
        return return_tuple

    #  from meerschaum.utils.pool import get_pool
    #  pool = get_pool('ThreadPool', workers=workers)
    
    from multiprocessing import cpu_count
    from multiprocessing.pool import ThreadPool as Pool
    if workers is None: workers = cpu_count()
    pool = Pool(workers)

    results = pool.map_async(sync_pipe, pipes)
    results = results.get()
    if results is None:
        warn(f"Failed to fetch results from syncing Pipes.")
        succeeded_pipes = []
        failed_pipes = pipes
        results_dict = dict([(p, (False, f"Could not fetch sync result for Pipe '{p}'")) for p in pipes])
    else:
        ### determine which Pipes failed to sync
        pipe_indices = [i for p, i in enumerate(pipes)]
        succeeded_pipes = [pipe_indices[i] for i, r in enumerate(results) if r[0]]
        failed_pipes = [pipe_indices[i] for i, r in enumerate(results) if not r[0]]
        results_dict = dict([(p, r) for p, r in zip(pipe_indices, results)])

    if len(failed_pipes) > 0:
        print("\n" + f"Failed to sync Pipes:")
        for p in failed_pipes: print(f"  - {p}")

    if len(succeeded_pipes) > 0:
        success_msg = "\nSuccessfully synced Pipes:"
        if unblock: success_msg = "\nSuccessfully spawned threads for Pipes:"
        print(success_msg)
        for p in succeeded_pipes:
            print(f"  - {p}")

    if debug:
        import pprintpp
        dprint("\n" + f"Return values for each Pipe:")
        pprintpp.pprint(results_dict)

    return succeeded_pipes, failed_pipes

def _sync_pipes(
        loop : bool = False,
        min_seconds : int = 1,
        debug : bool = False,
        **kw
    ) -> tuple:
    """
    Fetch new data for Pipes
    """
    from meerschaum.utils.debug import dprint
    import time
    run = True
    msg = ""
    cooldown = 2 * (min_seconds + 1)
    while run:
        lap_begin = time.time()
        try:
            success, fail = _pipes_lap(
                min_seconds = min_seconds,
                debug = debug,
                **kw
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            from meerschaum.utils.warnings import warn
            warn(f"Failed to sync all pipes. Waiting for {cooldown} seconds, then trying again.", stacklevel=2)
            time.sleep(cooldown)
            cooldown = int(cooldown * 1.5)
            continue
        cooldown = 2 * (min_seconds + 1)
        lap_end = time.time()
        msg = (
            "\n" + f"It took {round(lap_end - lap_begin, 2)} seconds to sync {len(success) + len(fail)} pipes" + "\n" + 
            f"  ({len(success)} succeeded, {len(fail)} failed)."
        )
        print(msg)
        if min_seconds > 0 and loop:
            print("\n" + f"Sleeping for {min_seconds} second" + ("s" if abs(min_seconds) != 1 else ""))
            time.sleep(min_seconds)
        run = loop
    return True, msg

### NOTE: This must be the final statement of the module.
###       Any subactions added below these lines will not
###       be added to the `help` docstring.
from meerschaum.utils.misc import choices_docstring as _choices_docstring
sync.__doc__ += _choices_docstring('sync')

