import edstan
import pandas

# Import data as a pandas data frame
spelling = pandas.read_csv('spelling.csv')
words = ['infidelity', 'panoramic', 'succumb', 'girder']

# Use the response matrix to create an EdstanData instance
ed_1 = edstan.EdstanData(response_matrix = spelling[words])

# Fit the Rasch model
fit_1 = ed_1.fit_model('rasch', iter = 200, chains = 4)

# Print results
ed_1.print_from_fit(fit_1)