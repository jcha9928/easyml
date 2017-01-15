#!/bin/bash

# Set environment to exit with any non-zero exit codes
set -e

if [ ${TASK} == "r_test" ]; then
    # Not sure what this export does
    export _R_CHECK_TIMINGS_=0
    
    # Install R for OSx
    wget https://cran.rstudio.com/bin/macosx/R-latest.pkg  -O /tmp/R-latest.pkg
    sudo installer -pkg "/tmp/R-latest.pkg" -target /
    
    # Install devtools
    Rscript -e "install.packages('devtools', repo = 'https://cran.rstudio.com')"
    
    # Install package dependencies
    cd R
    Rscript -e "library(devtools); library(methods); options(repos=c(CRAN='https://cran.rstudio.com')); install_deps(dependencies = TRUE)"
    Rscript -e 'install.packages("roxygen2")'
    # Build package
    cd ..
    R CMD INSTALL R
    
    # Run tests
    cd R
    Rscript -e "devtools::test()" || exit -1
    Rscript tests/travis/r_vignettes.R
    
    # If successful this far, submit to test coverage and exit with exit 
    # code 0 (sucess).
    Rscript -e "library(covr); codecov()"
    exit 0
fi

if [ ${TASK} == "python_test" ]; then
    # Install Python?
    
    # Run tests
    python3 -m nose tests/python/unittest || exit -1
    
    # If successful this far, submit to test coverage and exit with exit 
    # code 0 (sucess).
    exit 0
fi
