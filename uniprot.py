#!/usr/bin/env python3

import argparse
import pandas as pd
import re
import requests
import sys

# rettype = uilist pour ne pas avoir à itérer comme un connard


def create_dataframe(file):
    data = {"gs": [], "orga": []}

    with open(file, "r") as f:
        for line in f.readlines():
            data["gs"].append(line.strip().split(",")[0])
            data["orga"].append(line.strip().split(",")[1])

    df = pd.DataFrame(data)

    return df


def get_uniprot_id(df):
    ids = [
        ['organism_name:"' + y + '"', "gene_exact:" + x]
        for x, y in zip(df["gs"], df["orga"])
    ]
    uni_id = []
    uni_name = []

    for id in ids:
        url = f"https://rest.uniprot.org/uniprotkb/search?query={id[0]}+{id[1]}&format=json"

        r = requests.get(url)

        decoded = r.json()

        uni_id.append(decoded["results"][0]["primaryAccession"])
        try:
            uni_name.append(
                decoded["results"][0]["proteinDescription"]["recommendedName"][
                    "fullName"
                ]["value"]
            )
        except KeyError:
            uni_name.append(
                "No full name"
            )  # A corriger car sans doute un nom quelque part

    df["uni_id"] = uni_id
    df["uni_name"] = uni_name

    return df


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--gene_symbol", help="Gene Symbol list", default="GeneSymbols_2.txt"
    )

    args = parser.parse_args()

    df = create_dataframe(args.gene_symbol)

    df = get_uniprot_id(df)

    print(df)


if __name__ == "__main__":
    main(sys.argv)
