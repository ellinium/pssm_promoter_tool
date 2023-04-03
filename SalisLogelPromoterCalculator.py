import random
import pandas as pd
from datetime import datetime
from Bio.Seq import Seq
import pssm_util

if __name__ == "__main__":
    from dask.distributed import Client, LocalCluster
    cluster = LocalCluster()  # Launches a scheduler and workers locally
    client = Client(cluster)

if __name__ == "__main__":

    start_time = datetime.now()
    salis_calc_run_num = 0

    #sequence = "".join([random.choice(['A','G','C','T']) for x in range(1000)])
    sequence = "".join([random.choice(['A','G','C','T']) for x in range(100)])

    sequence = "TCTATGCTCCAGGGCGATTAGGGAACAGCGTGTTGCTGGTCAGTAGTGTACCCTAGCCCACATAGCTACTTTTACTTCGTCCGTTCAGCGGACAAACGCT"
    #sequence = "ATGGTACGCTGGACTTTGTGGGATACCCTCGCTTTCCTGCTCCTGTTGAGTTTATTGCTGCCGTCATTGCTTATTATGTTCATCCCGTCAACATTCAAACGGCCTGTCTCATCATGGAAGGCGCTGAATTTACGGAAAACATTATTAATGGCGTCGAGCGTCCGGTTAAAGCCGCTGAATTGTTCGCGTTTACCTTGCGTGTACGCGCAGGAAACACTGACGTTCTTACTGACGCAGAAGAAAACGTGCGTCAAAAATTACGTGCGGAAAGAATGA"
    #sequence = "ATGAGTCAAGTTACTGAACAATCCGTACGTTTCCAGACCGCTTTGGCCTCTATTAAGCTCATTCAGGCTTCTGCCGTTTTGGATTTAACCGAAGATGATTTCGATTTTCTGACGAGTAACAAAGTTTGGATTGCTACTGACCGCTCTCGTGCTCGTCGCTGCGTTGAAGCTTGCGTTTACGGTACGCTGGACTTTGTGGGATACCCTCGCTTTCCTGCTCCTGTTGAGTTTATTGCTGCCGTCATTGCTTATTATGTTCATCCCGTCAACATTCAAACGGCCTGTCTCATCATGGAAGGCGCTGAATTTACGGAAAACATTATTAATGGCGTCGAGCGTCCGGTTAAAGCCGCTGAATTGTTCGCGTTTACCTTGCGTGTACGCGCAGGAAACACTGACGTTCTTACTGACGCAGAAGAAAACGTGCGTCAAAAATTACGTGCGGAGGGTGTGATGTAA"
    #sequence = "atgtctaaaggtaaaaaacgttctggcgctcgccctggtcgtccgcagccgttgcgaggtactaaaggcaagcgtaaaggcgctcgtctttggtatgtaggtggtcaacaattttaa"

    sequence = str.upper(sequence)
    calc = pssm_util.Promoter_Calculator()
    calc.run(sequence, TSS_range = [0, len(sequence)])
    fwd_TSS_df, rev_TSS_df = calc.output()
    end_time = datetime.now()
    print('Duration of 1 salis calc run: {}'.format(end_time - start_time))

    #fwd_TSS_df = TSS_results_to_df(output['Forward_Predictions_per_TSS'])
    #rev_TSS_df = TSS_results_to_df(output['Reverse_Predictions_per_TSS'])

    fwd_TSS_df = fwd_TSS_df.drop_duplicates(subset=['hex35', 'hex10', 'spacer', 'ITR'], keep='last')
    rev_TSS_df = rev_TSS_df.drop_duplicates(subset=['hex35', 'hex10', 'spacer', 'ITR'], keep='last')

    fwd_TSS_df = fwd_TSS_df.sort_values(by = 'Tx_rate', ascending = False)
    rev_TSS_df = rev_TSS_df.sort_values(by = 'Tx_rate', ascending = False)

    fwd_TSS_df['AA_Promoter_35'] = fwd_TSS_df['hex35'].apply(lambda x: str(Seq(x).translate()))
    fwd_TSS_df = fwd_TSS_df[fwd_TSS_df['AA_Promoter_35'].str.contains('*', regex = False) == False]

    fwd_TSS_df['AA_Promoter_10'] = fwd_TSS_df['hex10'].apply(lambda x: str(Seq(x).translate()))
    fwd_TSS_df = fwd_TSS_df[fwd_TSS_df['AA_Promoter_10'].str.contains('*', regex = False) == False]

    rev_TSS_df['AA_Promoter_35'] = rev_TSS_df['hex35'].apply(lambda x: str(Seq(x).translate()))
    rev_TSS_df = rev_TSS_df[rev_TSS_df['AA_Promoter_35'].str.contains('*', regex = False) == False]

    rev_TSS_df['AA_Promoter_10'] = rev_TSS_df['hex10'].apply(lambda x: str(Seq(x).translate()))
    rev_TSS_df = rev_TSS_df[rev_TSS_df['AA_Promoter_10'].str.contains('*', regex = False) == False]

    #TOP 5 Tx_rate revords
    max_fwd_TSS_df = fwd_TSS_df.head(1)
    def_fwd_max_tx_rate = max_fwd_TSS_df['Tx_rate'].values[0]

    min_fwd_TSS_df = fwd_TSS_df.tail(1)
    def_fwd_min_tx_rate = min_fwd_TSS_df['Tx_rate'].values[0]


    max_rev_TSS_df = rev_TSS_df.head(1)
    def_rev_max_tx_rate = max_rev_TSS_df['Tx_rate'].values[0]

    min_rev_TSS_df = rev_TSS_df.tail(1)
    def_rev_min_tx_rate = min_rev_TSS_df['Tx_rate'].values[0]

    max_min_tx_rate_df = {"sequence": sequence, "max_fwd": def_fwd_max_tx_rate, "max_rev": def_rev_max_tx_rate, "min_fwd": def_fwd_min_tx_rate, "min_rev": def_rev_min_tx_rate}

    # for (TSS, result) in output['Forward_Predictions_per_TSS'].items():
    #     print("Fwd TSS: %s. TX Rate: %s. Calcs: %s" % (TSS, result['Tx_rate'], str(result) ))
    #     process_TSS_results(TSS, result)
    #
    # for (TSS, result) in output['Reverse_Predictions_per_TSS'].items():
    #     print("Rev TSS: %s. TX Rate: %s. Calcs: %s" % (TSS, result['Tx_rate'], str(result) ))
    #
    # print("Elapsed Time: ", time.time() - begin, " seconds.")


    #prm_df = process_promoters_nt(promoters_35, promoters_10, spacers)




    fwd_res_df_max = pssm_util.process_df_promoters(fwd_TSS_df.head(10), 'fwd', 'max', max_min_tx_rate_df)
    #fwd_res_df_max = pssm_util.process_df_promoters(fwd_TSS_df, 'fwd', 'max', max_min_tx_rate_df)
    #rev_res_df_max = pssm_util.process_df_promoters(rev_TSS_df.head(10), 'rev', 'max', max_min_tx_rate_df)
    rev_res_df_max = pssm_util.process_df_promoters(rev_TSS_df, 'rev', 'max', max_min_tx_rate_df)

    fwd_res_df_min = pssm_util.process_df_promoters(fwd_TSS_df.tail(10), 'fwd', 'min', max_min_tx_rate_df)
    #fwd_res_df_min = pssm_util.process_df_promoters(fwd_TSS_df, 'fwd', 'min', max_min_tx_rate_df)
    rev_res_df_min = pssm_util.process_df_promoters(rev_TSS_df.tail(10), 'rev', 'min', max_min_tx_rate_df)
    #rev_res_df_min = pssm_util.process_df_promoters(rev_TSS_df, 'rev', 'min', max_min_tx_rate_df)


    #TODO:  keep original_TSS
    max_fwd_TSS_df = fwd_res_df_max.loc[fwd_res_df_max['Tx_rate'].astype(float) >= float(def_fwd_max_tx_rate)]
    max_rev_TSS_df = rev_res_df_max.loc[rev_res_df_max['Tx_rate'].astype(float) >= float(def_rev_max_tx_rate)]

    min_fwd_TSS_df = fwd_res_df_min.loc[fwd_res_df_min['Tx_rate'].astype(float) <= float(def_fwd_min_tx_rate)]
    min_rev_TSS_df = rev_res_df_min.loc[rev_res_df_min['Tx_rate'].astype(float) <= float(def_rev_min_tx_rate)]

    res_final_df_max = pd.concat([max_fwd_TSS_df, max_rev_TSS_df], ignore_index=True, sort=False)
    res_final_df_min = pd.concat([min_fwd_TSS_df, min_rev_TSS_df], ignore_index=True, sort=False)
    #res_final_df = res_final_df.drop_duplicates()
    res_final_df_max = res_final_df_max.drop_duplicates(
        subset=['hex35', 'hex10', 'Tx_rate', 'ITR', 'original_TSS', 'direction'],
        keep='last').reset_index(drop=True)


    res_final_df_min = res_final_df_min.drop_duplicates(
        subset=['hex35', 'hex10', 'Tx_rate', 'ITR', 'original_TSS', 'direction'],
        keep='last').reset_index(drop=True)

    res_final_df_max['AA_hex35'] = res_final_df_max['hex35'].apply(lambda x: str(Seq(x).translate()))
    res_final_df_min['AA_hex35'] = res_final_df_min['hex35'].apply(lambda x: str(Seq(x).translate()))
    res_final_df_max['AA_hex10'] = res_final_df_max['hex10'].apply(lambda x: str(Seq(x).translate()))
    res_final_df_min['AA_hex10'] = res_final_df_min['hex10'].apply(lambda x: str(Seq(x).translate()))

    #+PSSM values
    res_final_df_max['PSSM_hex35'] = res_final_df_max['hex35'].apply(lambda x: pssm_util.calc_PSSM(x, '35'))
    res_final_df_max['PSSM_hex10'] = res_final_df_max['hex35'].apply(lambda x: pssm_util.calc_PSSM(x, '10'))
    res_final_df_min['PSSM_hex35'] = res_final_df_max['hex10'].apply(lambda x: pssm_util.calc_PSSM(x, '35'))
    res_final_df_min['PSSM_hex10'] = res_final_df_max['hex10'].apply(lambda x: pssm_util.calc_PSSM(x, '10'))

    #perm_prom_pssm_df['PSSM_Promoters_perm'] = perm_prom_pssm_df['Promoters_perm_nt'].apply(lambda x: calc_PSSM(x, type))

    #res_final_df_max.to_csv('SalisLogelPromoterCalculator_MAX_results.csv')
    #res_final_df_min.to_csv('SalisLogelPromoterCalculator_MIN_results.csv')

    print(sequence)

    res_final_df_max_fwd_df = res_final_df_max.loc[res_final_df_max["direction"] == 'fwd']
    new_max_fwd_Tx_rate_df = res_final_df_max_fwd_df.sort_values(by='Tx_rate', ascending=False)
    new_max_fwd_Tx_rate = new_max_fwd_Tx_rate_df['Tx_rate'].head(1).values[0]


    res_final_df_min_fwd_df = res_final_df_min.loc[res_final_df_max["direction"] == 'fwd']
    new_min_fwd_Tx_rate_df = res_final_df_min_fwd_df.sort_values(by='Tx_rate', ascending=False)
    new_min_fwd_Tx_rate = new_min_fwd_Tx_rate_df['Tx_rate'].tail(1).values[0]


    res_final_df_max_rev_df = res_final_df_max.loc[res_final_df_max["direction"] == 'rev']
    new_max_rev_Tx_rate_df = res_final_df_max_rev_df.sort_values(by='Tx_rate', ascending=False)
    new_max_rev_Tx_rate = new_max_rev_Tx_rate_df['Tx_rate'].head(1).values[0]

    res_final_df_min_rev_df = res_final_df_min.loc[res_final_df_min["direction"] == 'rev']
    new_min_rev_Tx_rate_df = res_final_df_min_rev_df.sort_values(by='Tx_rate', ascending=False)
    new_min_rev_Tx_rate = new_min_rev_Tx_rate_df['Tx_rate'].tail(1).values[0]

    column_list = ["new_sequence", "promoter_sequence", "TSS", "Tx_rate", "UP", "hex35", "PSSM_hex35", "AA_hex35", "spacer", "hex10", "PSSM_hex10", "AA_hex10", "disc", "ITR", "dG_total", "dG_10", "dG_35", "dG_disc", "dG_ITR", "dG_ext10", "dG_spacer", "dG_UP", "dG_bind",  "UP_position", "hex35_position", "spacer_position", "hex10_position", "disc_position"]

    print("The minimum transcription rate for the sequence (forward) " + str(def_fwd_min_tx_rate))
    if len(res_final_df_min_fwd_df) > 1:
        if float(new_min_fwd_Tx_rate) < float(def_fwd_min_tx_rate):
            print ("can be decreased up to " + str(new_min_fwd_Tx_rate))
            print("using the following promoters:")
            res_final_df_max_fwd_df.to_csv("SalisLogelPromoterCalculator_MIN_FWD_results.csv", columns = column_list)
    else:
        print(" cannot be further decreased")

    print("The minimum transcription rate for the sequence (reverse) " + str(def_rev_min_tx_rate))
    if len(res_final_df_min_rev_df) > 1:
        if float(new_min_rev_Tx_rate) < float(def_rev_min_tx_rate):
            print ("can be decreased up to " + str(new_min_rev_Tx_rate))
            print("using the following promoters:")
            res_final_df_max_fwd_df.to_csv("SalisLogelPromoterCalculator_MIN_REV_results.csv", columns = column_list)

    else:
        print(" cannot be further decreased")
    print("The maximum transcription rate for the sequence (forward) " + str(def_fwd_max_tx_rate))
    if len(res_final_df_max_fwd_df) > 1:
        if float(new_max_fwd_Tx_rate) > float(def_fwd_max_tx_rate):
            print ("can be increased up to " + str(new_max_fwd_Tx_rate))
            print("using the following promoters:")
            res_final_df_max_fwd_df.to_csv("SalisLogelPromoterCalculator_MAX_FWD_results.csv", columns = column_list)

    else:
        print(" cannot be further increased")

    print("The maximum transcription rate for the sequence (reverse) " + str(def_rev_max_tx_rate))
    if len(res_final_df_max_rev_df) > 1:
        if float(new_max_rev_Tx_rate) > float(def_rev_max_tx_rate):
            print ("can be increased up to " + str(new_max_rev_Tx_rate))
            print("using the following promoters:")
            res_final_df_max_fwd_df.to_csv("SalisLogelPromoterCalculator_MAX_REV_results.csv", columns = column_list)

    else:
        print(" cannot be further increased")




    print("Mac Tx rate FWD = " + str(def_fwd_max_tx_rate))
    print("Mac Tx rate REV = " + str(def_rev_max_tx_rate))
    print("Min Tx rate FWD = " + str(def_fwd_min_tx_rate))
    print("Min Tx rate REV = " + str(def_rev_min_tx_rate))



    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

# +BOTTOM sequences
#Display synonymous only if Tx_rate more than it was