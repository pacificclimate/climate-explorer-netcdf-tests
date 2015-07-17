# climate-explorer-netcdf-tests
A collection of netCDF4 performance tests

Use the included docker build to help create a development environment

    docker build -t pcic/climate-explorer . # Optional, will pull the image from docker hub by default
    docker run -d -p 127.0.0.1:<port>:8888 --name ipython -v <absolute_path_to_code_direcotry>:/app [-v <path_to_large_storage_dir>:/app/tmp] pcic/climate-explorer

Run `docker port ipython` to get the port being redirected.

## Host Cache Issues

Files which are dynimiacally generated in the docker container, closed, the read for performance tests may or may not be cached by the host OS. This creates unrealistic results reading directly from memory. Since the container does not have the permissions for this, some coordination is required between the host. This solution requires that the application path is mounted as a volume within the container per the above `run` command.

### Host

`clear_host_cache.sh` must be run with superuser priviledges at the application root. This looks for a file <application_root>/cc_sig.tmp. When detected, it clears the host cache and then deletes the file.

### Container

Calling `clear_host_cache()` creates the file <application_root>/cc_sig.tmp and then continuously tries to stat that file. When the file is deleted (cache cleared) control is returned to the caller.
