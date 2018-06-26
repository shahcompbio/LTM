import os
import shutil
from ltm import ltm

ltm_directory = os.path.realpath(os.path.dirname(ltm.__file__))


def move_cellscape(outfile):
    cellscape_rmarkdown = os.path.join(ltm_directory, 'cellscape.Rmd')

    shutil.copy(cellscape_rmarkdown, outfile)

