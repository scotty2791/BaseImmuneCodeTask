import mhcflurry_wrapper as mhc

mhc.run_wrapper(mhc.run_mhcflurry_predict_scan(
    "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHS", "HLA-A*02:01", "./combinedcmd.csv"))

command = mhc.run_mhcflurry_predict_scan(
    "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHS", "HLA-A*02:01", "./splitcmd.csv")
mhc.run_wrapper(command)
