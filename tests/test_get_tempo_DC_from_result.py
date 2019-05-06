import h5py
from numpy import mean, floor

temp_file_bpm = h5py.File('/archive/WASABI/media/results/2ff01106-1200-4d8d-a245-6a9f3f8525e6/4395e477-d61c-446b-b2e5-332ed858c9a2.hdf5')
grp_bpm = temp_file_bpm['./aubio_temporal.bpm/']
dataset_bpm = grp_bpm['data_object']

temp_file_dc = h5py.File('/archive/WASABI/media/results/2ff01106-1200-4d8d-a245-6a9f3f8525e6/376d888b-9846-4e00-a81c-a9a246147a5a.hdf5')
grp_dc = temp_file_dc['./mean_dc_shift/']
dataset_dc = grp_dc['data_object']

# mean BPM of the entire track
print('BPM :')
print(int(floor(mean(dataset_bpm['value'][()]))))

# DC
print('DC :')
print(dataset_dc['value'][()][0])
