# Input data

This directory contains all input files required by `2609_fig/main_fig.ipynb`, together with `2610_all_data.csv`. See `manifest.csv` for the file list and checksums. The input paths in the notebooks are kept as they were in the original analysis.

- Latest version (`2609_fig/main_fig.ipynb`): `data_root` points to the original absolute path. Set it to this directory before running the notebook.
- Histopathology analysis (`legacy/fig_submisson_HEandAD.ipynb`): reads the npy and pickle files in `workspace/result_v5/` and the TIF files in `workspace/HE_240205_iwasaka/` through relative paths from the repository root. These original files are not included in this repository.
- The histopathology notebook also imports the external `data_handler` module after adding `/workspace` to the module search path. This external dependency is not included.

The notebooks have not been re-run with the files in this directory. `main_fig.ipynb` writes `immune_stats.csv` and `gage_rawdata.csv` to `data_root`; these are outputs, not missing inputs.

## RNA-seq expression data: res_annotation.csv

`res_annotation.csv` is an expression matrix with genes in rows and samples in columns. It was produced as follows, based on the code we used:

1. `RNAseq/tximport/main.R` or `main_noconv.R` reads the Salmon quantification results and saves `$counts` from `summarizeToGene(..., countsFromAbundance = "scaledTPM")` to per-sample `res_gene/*.csv` files. These values are counts generated with the tximport scaledTPM option; they are neither ordinary TPM values nor Z-scores. The two R scripts differ in how the tx2gene table is constructed, and which one was used has not been confirmed.
2. `RNAseq/salmon/integrate.py` outer-joins the per-sample CSV files column-wise and saves them as the tab-separated `expression.txt` by default.
3. `RNAseq/ref/230528_geneplot.ipynb` reads `res_summary/expression.txt` and the BioMart table `mouse_geneID_geneNAME.csv`.
4. The version suffix (after the dot) is removed from the gene IDs, and `Gene stable ID` is converted to `Gene name` using the table. Rows that cannot be mapped to a gene name are removed.
5. Multiple rows mapped to the same gene name are aggregated by the per-sample **median** (not the sum or mean).
6. Columns whose names contain `good_out` are removed. According to the saved notebook output, 72 columns remain.
7. The resulting `df_fix` is saved as `res_annotation.csv`. This save step comes before the step that renames the samples using separate metadata.

In summary, `res_annotation.csv` is **an expression matrix of tximport scaledTPM-derived counts, annotated with gene names, with genes sharing the same name aggregated by the median, and restricted to the target samples**. No log transformation or Z-score standardization is applied before saving. `main_fig.ipynb` applies log2(x + 1) transformation and per-gene standardization as needed in each analysis, so do not apply these transformations to the input CSV in advance.

### Scope of verification and notes for re-analysis

- The processing steps above were confirmed by reading the RNA-seq processing code, which is not included in this repository. The BioMart table is not included either.
- The save line in the geneplot notebook, `#df_fix.to_csv("res_annotation.csv")`, is currently commented out. The code documents the procedure but does not by itself prove that this save was executed.
- The values and sample correspondence between `expression.txt` and `res_annotation.csv` have not been fully cross-checked. The R script used, the versions of Salmon and tximport, the reference sequences, the tx2gene table, and the version of the BioMart table have not been recorded here.
- `main_fig.ipynb` renames the columns sequentially using the metadata. For re-analysis, the sample order of the expression matrix and the metadata must match, not just the number of samples.

## Check of res_annotation.csv (2026-10-17)

`res_annotation.csv` contains 54,154 genes × 72 samples. The first column is `gene`, and the sample columns are DRR IDs. There are no duplicated gene or sample names, and no missing, non-finite, or negative values.

The 100 values displayed in the saved `df_fix.head()` output of `230528_geneplot.ipynb` match this file to the displayed precision (six decimal places). The full matrix has not been recomputed from `expression.txt`. Column sums range from about 16.1 to 27.7 million, unlike ordinary TPM (column sum of 1 million), which is consistent with the scaledTPM-derived counts described above.

The columns are not sorted by DRR ID; the last three are DRR461044, DRR461062, and DRR461080. Do not reorder the columns, as the analysis results depend on this order.

SHA-256: `262341a8258a6214efdbccc76c083c0e039a56350a930994d53b06b49fa8695a`

## Sample information and blood biochemistry: 2610_all_data.csv

A table with one row per sample (82 rows, 16 columns): 18 Control, 32 TAA, and 32 MDA samples, with day values of 1, 2, 3, 4, and 8. `No.` and `ID` are unique.

| Column | Description |
| --- | --- |
| No. | Sequential number in the table |
| ID | Sample identifier (e.g., 1C1, 8M3) |
| group | Experimental group: Control, TAA, or MDA |
| day | Day category: 1, 2, 3, 4, or 8. The reference day is not stated in the CSV |
| BW | Body weight. The unit is not stated in the CSV |
| ALT / AST | Alanine / aspartate aminotransferase |
| TBIL | Total bilirubin |
| TCHO | Total cholesterol |
| HDL | HDL cholesterol |
| TG | Triglycerides |
| ALP | Alkaline phosphatase |
| GGT | γ-Glutamyltransferase |
| GGT_at | `@` indicates a value below the lower limit of quantification; kept distinct from blank cells |
| water batch | Batch of prepared drinking water: tap water, TAA 400, TAA 1000, MDA 400, or MDA 1000. This column does not indicate the dose |
| rnaseq_file | DRR ID corresponding to a column of the expression matrix; `No File` if there is no corresponding RNA-seq data |

The units of the biochemistry values are not stated in the CSV. The plotting code labels ALT, AST, and ALP in U/l and TBIL, TCHO, HDL, and TG in mg/dl.

### Missing values and sample correspondence

Blank cells in the numeric columns: TBIL 1, TCHO 1, HDL 2, TG 3, ALP 1, and GGT 1. `GGT_at` has 5 blank cells. Do not replace blanks with zero; specify how missing values are handled in each analysis.

Ten samples have `rnaseq_file` = `No File`, and the DRR IDs of the remaining 72 samples are unique. They match the 72 columns of `res_annotation.csv` both as a set and in order after removing the `No File` rows. The last three samples are:

| ID | rnaseq_file |
| --- | --- |
| 8M3 | DRR461044 |
| 8M5 | DRR461062 |
| 8M6 | DRR461080 |

To join the tables, use `rnaseq_file` and the column names of the expression matrix, not row numbers or IDs. Example:

```python
from pathlib import Path
import pandas as pd

data_dir = Path("data")
metadata = pd.read_csv(data_dir / "2610_all_data.csv")
expression = pd.read_csv(data_dir / "res_annotation.csv", index_col=0)
rna_metadata = metadata.loc[metadata["rnaseq_file"] != "No File"].copy()
assert rna_metadata["rnaseq_file"].notna().all()
assert rna_metadata["rnaseq_file"].is_unique
assert expression.columns.is_unique
assert set(rna_metadata["rnaseq_file"]) == set(expression.columns)
rna_metadata = rna_metadata.set_index("rnaseq_file").loc[expression.columns]
assert rna_metadata.index.tolist() == expression.columns.tolist()
```

This table has a different column layout from the metadata CSV files read by the latest notebook. Because the notebook selects columns by position, it cannot simply be swapped in by changing the file name.

Checked on 2026-10-17. SHA-256: `802fe56ed98d4ada75566d27977612df01c8151452a042b5fe9bb247129ad172`

The BW, ALT, and AST values of six MDA day 1 samples in some of the files contain a transcription error. See the "Known data error" section of the root README for details.
