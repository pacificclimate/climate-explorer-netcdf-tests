# climate-explorer-netcdf-tests
A collection of netCDF4 performance tests

Use the included docker build to help create a development environment

    docker build -t pcic/climate-explorer . # Optional, will pull the image from docker hub by default
    docker run -d -P --name ipython -v <absolute_path_to_notebooks_directory>:/app/notebooks pcic/climate-explorer

Run `docker port ipython` to get the port being redirected
