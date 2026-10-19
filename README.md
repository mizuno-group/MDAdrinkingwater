# MDAdrinkingwater

This repository contains the figure-generation code for our paper on the TAA and MDA drinking-water models, together with the blood biochemistry and RNA-seq expression data used in the analyses.

# Note
This repository is a research resource of the [Mizuno group](https://github.com/mizuno-group). It provides the input data and the notebooks with their saved outputs. All nine input files required by the latest notebook are included in `data/`. Re-running the notebooks with these files has not been verified.
Please contact tadahaya[at]gmail.com before publishing your paper using the contents of this repository.  

## Authors
- [Takumi Iwasaka](https://github.com/T-IWASAKA)  
    - main contributor  
- [Tadahaya Mizuno](https://github.com/tadahayamiz)  
    - correspondence  

## Contact
If you have any questions or comments, please feel free to create an issue on github here, or email us:  
- iwasaka14[at]g.ecc.u-tokyo.ac.jp  
- tadahaya[at]gmail.com  
    - lead contact  

## Repository structure

The final figure-generation notebooks are grouped in `notebooks/`; see [notebooks/README.md](notebooks/README.md) for their roles. The original environment record is in `environment/env.txt`.

The latest version of the paper figures is `notebooks/main_fig.ipynb`. `notebooks/fig_submisson_HEandAD.ipynb` is kept as a reference for the histopathological image analysis, which is the source of the abnormal patch ratios shown in Fig 2e. The statistical analyses, plotting code, figure names, and saved cell outputs have not been changed, except that the package installation log at the top of the HEandAD notebook has been removed.

| Notebook | Role | Figure output directory |
| --- | --- | --- |
| `notebooks/main_fig.ipynb` | Figures of the latest version of the paper | `results/main_fig/` |
| `notebooks/fig_submisson_HEandAD.ipynb` | Anomaly detection and patch extraction on histopathology images | `results/histopathology/` |

Figure file names and save settings are unchanged. See `notebooks/figure_inventory.csv` for the list of figures. The `results/` directories are created when the notebooks are run; the figures have not been regenerated for this release.

## Running the notebooks

Set the working directory of the Python kernel to the root of this repository, not to the subdirectory that contains the notebook. The path-setup cell checks this condition. If necessary, run the following in a separate cell before running the notebook (this temporary cell does not need to be saved):

```python
import os
os.chdir("/path/to/MDAdrinkingwater")
```

In `notebooks/main_fig.ipynb`, `data_root` points to the repository `data/` directory. Inputs are read from `raw/` and `references/`; generated statistics tables are saved in `results/tables/`.

The latest notebook uses the bundled `notebooks/utils/`. The external dependencies of the histopathology notebook are described in `data/README.md`. `environment/env.txt` is the `pip list` output of the original environment and is kept as a record; it is not a lock file.

## Saved outputs

Figure outputs, execution counts, and cell order are preserved; the previously removed HEandAD installation log is the exception. They are the results of the original runs. Re-running in the current environment and reproducing identical figures has not been verified. The notebooks can be viewed without clearing outputs or re-running.

Known inconsistencies are described in the "Known data error" and "Known inconsistency" sections at the end of this README. To keep the published figures intact, the analysis and plotting code have not been modified; path settings have been updated.

## Data

- [data/README.md](data/README.md): column descriptions, processing of the scaledTPM-derived expression values, missing values, and sample correspondence.
- [data/manifest.csv](data/manifest.csv): size, SHA-256, and shape of each data file.

`2610_all_data.csv` and `res_annotation.csv` contain the same 72 RNA-seq samples in the same order. However, `2610_all_data.csv` has a different column layout from the metadata CSV files read by the notebook, so it cannot be used as a drop-in replacement. To preserve the analysis and saved outputs, the notebook still reads the original metadata files.

All inputs required by the latest notebook are included in `data/`. Note that the BW, ALT, and AST values of six MDA day 1 samples contain a transcription error (see the next section).

## Known data error (BW, ALT, and AST of MDA day 1)

In `230528_DrinkingWaterModel_rawdata_v2.csv` and `230605_data_blood_facs.csv`, the BW, ALT, and AST values of 1M1–1M6 (MDA day 1) were mistakenly copied from 1T1–1T6 (TAA day 1). The correct values are given in `240111_DrinkingWaterModel_rawdata_v6.csv` and `2610_all_data.csv`. See [data/metadata_value_differences.csv](data/metadata_value_differences.csv) for the differences between the two sets of files.

To keep the correspondence with the published analyses and figures, the files containing the error are provided as is.

- Affected: Fig 5b (ALT coloring in the RNA-seq META visualization). Five samples (1M1, 1M2, 1M3, 1M5, and 1M6) are colored with incorrect ALT values (1M4 is excluded from the analysis).
- Not affected: Fig S3 (blood biochemistry) uses the correct values. The FACS figures (Fig 4 and S4) use only the FACS fractions.

When using BW, ALT, or AST in a new analysis, use the values in `240111_DrinkingWaterModel_rawdata_v6.csv` or `2610_all_data.csv`.

## Known inconsistency (samples 24 and 25 in Fig 2e)

The order of histopathology slides No. 24 and No. 25 was swapped when the images were acquired. The correct assignment is No. 24 = MDA day 7 and No. 25 = TAA day 28. `notebooks/fig_submisson_HEandAD.ipynb` swaps the groups of these two samples accordingly. Fig 2e, the patch PCA, and the extracted patch images use the same (correct) assignment.

In contrast, the "ad p val" cell in `notebooks/main_fig.ipynb` does not reflect this swap and performs one-sided t-tests treating No. 24 as TAA day 28 and No. 25 as MDA day 7. Therefore, the t and p values printed by that cell for TAA day 28 and MDA day 7 differ from those printed by the Fig 2e plotting cell.

| Group | "ad p val" cell (incorrect) | Fig 2e plotting cell (correct) |
| --- | --- | --- |
| TAA day 28 | t=1.440, p=0.123 | t=1.846, p=0.081 |
| MDA day 7 | t=4.304, p=0.0115 | t=6.233, p=0.0042 |

The significance decisions (α=0.05) are the same in both cases, so the asterisks in Fig 2e are not affected. The values from that cell are not reported in the main text or figure legends of the paper. To keep the saved outputs intact, the notebook has not been modified.

## Known inconsistency (y-axis labels of Fig S3-1 and S3-2)

For Fig S3-1 (ALT) and S3-2 (AST) in `notebooks/main_fig.ipynb`, `"ALP (U/l)"` is passed as the `title` argument of `value_plot`, so the y-axis label of the saved figures reads "ALP (U/l)". The plotted values are ALT and AST, respectively, as indicated by the figure titles, and the correct y-axis labels are "ALT (U/l)" and "AST (U/l)". The plotted values and statistical analyses are not affected. To keep the saved outputs intact, the notebook has not been modified.


## Data organization

`data/raw/` preserves source files. `data/processed/` provides English-documented, reuse-ready copies. `data/references/` holds gene sets. See [data/README.md](data/README.md) for paths and provenance. Raw means preserved source files, not necessarily unprocessed measurements.
