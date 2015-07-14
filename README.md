# climate-explorer-netcdf-tests
A collection of netCDF4 performance tests

Use the included docker build to help create a development environment

    docker build -t pcic/climate-explorer . # Optional, will pull the image from docker hub by default
    docker run -d -p 127.0.0.1:<port>:8888 --name ipython -v <absolute_path_to_code_direcotry>:/app pcic/climate-explorer

Run `docker port ipython` to get the port being redirected

## Performance tests involving reading from rotating media require that the host cache be cleared before the read.  

Docker containers do not have permissions to do this, so a workaround solution has been made as follows:

An additional directory is added, called 'watch', which is made common to both the host and the Docker container, where a temporary file is created and modified by the iPython scripts running within the container. This file is used as a signal to a script with root privileges running on the host to trigger it to carry out a system file cache clear operation, and then delete the same temporary file to signal back to the iPython notebook that the operation is complete.

### The details:
The function clear_host_cache() was added to the meters module, which is used to create, open, and modify the temporary file 'cc_sig.tmp' in the '/app/util/watch' directory in the container (linked to the 'watch' directory on the host using the -v option when starting up the Docker container via 'docker run...'). When the file *mysteriously* disappears (done by the bash script on the host), it exits. 

The bash script clear_host_cache.sh is also in the 'util' directory of the repo, but is to be executed from the host side before running any iPython test scripts in the Docker container that require the cache to be cleared. It runs in continuous loop (until killed by ^C), checking for the 'cc_sig.tmp' file to change, then carries out a 'echo 3 >/proc/sys/vm/drop_caches' and deletes 'cc_sig.tmp' to signal back to 'clear_host_cache()' (running in the Docker container) that the operation is complete. The best way to invoke it is silently: '> sudo ./clear_host_cache.sh &> /dev/null' (it will complain verbosely at the beginning when 'cc_sig.tmp' does not exist).

Example invocation of the Docker container with the above implemented:
'sudo docker run -d -p 127.0.0.1:8887:8888 --name ipython -v /home/mfischer/code/climate-explorer/climate-explorer-netcdf-tests/:/app -v /mnt/storage/:/app/tmp -v /etc/localtime:/etc/localtime:ro pcic/climate-explorer' 
