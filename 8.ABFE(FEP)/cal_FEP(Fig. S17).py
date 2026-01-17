from alchemlyb.workflows import ABFE
import os
import pandas as pd

workflow = ABFE(units='kcal/mol', software='GROMACS', dir='xvg',
                prefix='md_', suffix='xvg', T=310, outdirectory='./')
workflow.run(skiptime=100, uncorr='dhdl', threshold=50,
             estimators=('MBAR', 'BAR', 'TI'), overlap='O_MBAR2.pdf',
             breakdown=True, forwrev=10)
summary = workflow.summary
summary.to_csv('summary.csv', index=False)

