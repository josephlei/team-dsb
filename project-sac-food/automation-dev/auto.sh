wget -O raw_data.csv http://data.saccounty.net/datasets/67343-restaurant-food-inspections.download/

ipython nbconvert --to python proc-raw-data.ipynb

python proc-raw-data.py