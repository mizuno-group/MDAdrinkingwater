# Reuse-ready data

## Contents and provenance

`sample_metadata.csv` contains 82 samples and 16 columns: 18 Control, 32 TAA, and 32 MDA samples. It is a sample-level integrated table, not a statistical summary. Only source headers were renamed; values, blank cells and row order are unchanged from ../raw/integrated/2610_all_data.csv. See column_dictionary.csv for the mapping and meanings.

`gene_expression_scaled_tpm.csv` contains 54,154 genes by 72 samples, plus a gene-name index column. It is byte-identical to ../raw/rnaseq/res_annotation.csv. Values are tximport scaledTPM-derived counts after gene-name mapping, per-sample median aggregation of duplicated gene names, and sample selection. They are neither ordinary TPM nor log-transformed or Z-standardized values. No new normalization was performed.

## Missing values, qualifiers and joining

Ten metadata rows have rnaseq_id = No File. The other 72 IDs are unique and match the expression columns in their existing order. The last three are DRR461044, DRR461062 and DRR461080. Join by ID, not by assumed row position.

Blank measurements remain blank; do not replace them with zero. The @ GGT qualifier denotes the lower quantification limit. Specify its treatment in any new analysis. drinking_water_batch identifies preparation batches, not doses. Measurement units and the day origin are not fully confirmed in source records; do not infer them from the renamed headers.

```python
from pathlib import Path
import pandas as pd

root = Path("data/processed")
metadata = pd.read_csv(root / "sample_metadata.csv")
expression = pd.read_csv(root / "gene_expression_scaled_tpm.csv", index_col=0)
samples = metadata.loc[metadata["rnaseq_id"] != "No File"].copy()
assert samples["rnaseq_id"].notna().all()
assert samples["rnaseq_id"].is_unique
assert expression.columns.is_unique
assert set(samples["rnaseq_id"]) == set(expression.columns)
samples = samples.set_index("rnaseq_id").loc[expression.columns]
assert samples.index.tolist() == expression.columns.tolist()
```

## Limitations

Metadata uses the corrected values documented in the root README, not the historical copied MDA day 1 measurements. This does not alter the published figures. The original tximport script/version and reference annotation versions have not been fully established. Original processing details and verification limits are in ../raw/README.md.
