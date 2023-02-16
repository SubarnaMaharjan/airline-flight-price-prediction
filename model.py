

import pickle

path = 'Model/flight_price_rf.pkl'
model = open(path, 'rb')
reg_rf = pickle.load(model)

reg_rf.predict()