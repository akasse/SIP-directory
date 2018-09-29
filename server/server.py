#!/usr/bin/python
#
# Description : 
#
# Author : thomas.boutry@x3rus.com
# Licence : GPLv3
# TODO :
############################################################################

# Argument :
#   # Exclusion user
#   # Exclusion repertoire
#   # Disable validation jenkins build file in directory

###########
# Modules #


import argparse                                    # Process command line argument
import sys
import os
import re
from gitBuildTriggerValidation import gitBuildTriggerValidation

#########
# Main  #


if __name__ == '__main__':

    # Set default value for last commit processed with success
 
