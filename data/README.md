# Data guide

## Choose your data

- **Published figure inputs:** `raw/` preserves source files, including historical metadata errors, for the original analysis.
- **New analyses:** `processed/` provides English-documented metadata and expression copies. See [processed/README.md](processed/README.md).
- **Reference gene sets:** `references/` contains the GO data used by GAGE.

Here, raw means the supplied source files preserved without value changes, not necessarily unprocessed instrument measurements. Many source tables have already been assembled or normalized. Processed does not mean that new normalization was performed.

## Original file locations

| File | Location relative to data/ |
| --- | --- |
| 230528_DrinkingWaterModel_rawdata_v2.csv | raw/rnaseq/230528_DrinkingWaterModel_rawdata_v2.csv |
| 230605_data_blood_facs.csv | raw/facs/230605_data_blood_facs.csv |
| 231020_dw_day14_fib_2309sample_v2 -  Quantification Cq Results.csv | raw/qpcr/231020_dw_day14_fib_2309sample_v2 -  Quantification Cq Results.csv |
| 231023_dw_day28_fib_2309sample -  Quantification Cq Results.csv | raw/qpcr/231023_dw_day28_fib_2309sample -  Quantification Cq Results.csv |
| 240111_DrinkingWaterModel_rawdata_v6.csv | raw/biochemistry/240111_DrinkingWaterModel_rawdata_v6.csv |
| 2610_all_data.csv | raw/integrated/2610_all_data.csv |
| drink_TAA_MDA_chronic.csv | raw/biochemistry/drink_TAA_MDA_chronic.csv |
| go_mouse_msigdb.pickle | references/go_mouse_msigdb.pickle |
| res_annotation.csv | raw/rnaseq/res_annotation.csv |
| waterdata.csv | raw/drinking_water/waterdata.csv |

## Reuse-ready files

| File | Source and transformation |
| --- | --- |
| processed/sample_metadata.csv | raw/integrated/2610_all_data.csv; column names converted to English snake_case only; values and row order unchanged |
| processed/gene_expression_scaled_tpm.csv | Byte-identical copy of raw/rnaseq/res_annotation.csv with a descriptive filename |

The duplicate expression matrix is intentional. `manifest.csv` records checksums, dimensions and source relationships. Detailed provenance is retained in [raw/README.md](raw/README.md).

## Known differences

Original RNA-seq metadata and FACS metadata retain copied BW/ALT/AST values for six MDA day 1 samples. The processed metadata uses the values from 2610_all_data.csv, consistent with the corrected biochemistry table. Do not substitute it into the published workflow without checking effects on figures. See the root README and [metadata_value_differences.csv](metadata_value_differences.csv).

The main notebook reads raw inputs and reference data. Generated immune_stats.csv and gage_rawdata.csv are written to results/tables/. No notebook was re-run during this reorganization.
