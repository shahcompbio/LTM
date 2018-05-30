import os
import pypeliner
import shutil

from scripts.LTM_main import ltm

scripts_directory = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'scripts')


def move_cellscape(outfile):
    cellscape_rmarkdown = os.path.join(scripts_directory, 'cellscape.Rmd')

    shutil.copy(cellscape_rmarkdown, outfile)

