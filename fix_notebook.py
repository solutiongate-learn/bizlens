import json

notebook_path = "notebooks/01_Quick_Start_Colab.ipynb"
with open(notebook_path, 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            if "quality_score:.1f" in line:
                line = line.replace("quality_score:.1f", "quality_score['overall_score']:.1f")
            elif "bz.diagnostic.detect_outliers(data[['sales']]" in line:
                line = line.replace("outliers = bz.diagnostic.detect_outliers(data[['sales']]", "outliers, _ = bz.diagnostic.detect_outliers(data['sales']")
            elif "len(outliers)" in line and "outliers, _" in "".join(new_source[-1:]):
                pass
            elif "bz.diagnostic.normality_test(data[['sales']])" in line:
                line = line.replace("data[['sales']]", "data['sales']")
            elif "ci['lower']" in line and "ci['upper']" in line:
                line = line.replace("ci['lower']", "ci[0]").replace("ci['upper']", "ci[2]")
            
            # For ANOVA
            if "bz.inference.anova_test(" in line:
                line = "anova_result = bz.inference.anova_test(\n"
            elif "data," in line and "group_col" in "".join(cell['source']):
                line = "    {region: data[data['region'] == region]['sales'] for region in data['region'].unique()}\n"
            elif "group_col='region'" in line:
                line = ""
            elif "value_col='sales'" in line:
                line = ""
                
            new_source.append(line)
        cell['source'] = new_source

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=2)
print("Notebook updated!")
