# -*- coding: utf-8 -*-
"""Get the chemical formulas for the structures
(used to plot the frequency of the elements)
"""
import pickle
import re
import time

from ccdc import io

from .utils import load_pickle


def get_chemical_formula(csd_reader, database_id):
    entry_object = csd_reader.entry(database_id)
    formula = entry_object.crystal.formula
    formula_dict = {}
    for elem in formula.split():
        count = int(re.search(r"\d+", elem).group())
        formula_dict[elem] = count

    return formula_dict


def main():
    # oxidation_parse_dict = load_pickle(
    #   "/home/kevin/Dropbox (LSMO)/proj62_guess_oxidation_states/oxidation_state_book/data/20190820-173457-csd_ox_parse_output.pkl"
    # )
    oxidation_reference_dict = load_pickle(
        "/home/kevin/Dropbox (LSMO)/proj62_guess_oxidation_states/mine_csd/20190921-142007-csd_ox_parse_output_reference.pkl"
    )

    database_ids = list(oxidation_reference_dict.keys())
    csd_reader = io.EntryReader("CSD")
    formula_dicts = {}
    for database_id in database_ids:
        formula_dicts[database_id] = get_chemical_formula(csd_reader, database_id)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_name = "-".join([timestr, "get_chemical_formulas"])
    with open(output_name + ".pkl", "wb") as filehandle:
        pickle.dump(formula_dicts, filehandle)


if __name__ == "__main__":
    main()
