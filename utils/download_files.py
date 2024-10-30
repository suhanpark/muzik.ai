from utils.gcs import GCS
import pickle
import os

if __name__ == '__main__':
    if os.path.exists('utils/gcs.pkl'):
        with open('utils/gcs.pkl', 'rb') as file:
            gcs = pickle.load(file)
    else:
        print('GCS FILE DOESNT EXIST')
        gcs = GCS()
        
        with open('utils/gcs.pkl', 'wb') as file:
            pickle.dump(gcs, file)
        print('GCS object created and saved.')
        
    print(gcs.download_midi())
    