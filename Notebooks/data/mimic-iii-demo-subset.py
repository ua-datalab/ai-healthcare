import pandas as pd

def load_lab_based_mimic_data(icustays_file, labevents_file, patients_file):
    """
    Load and preprocess data from ICUSTAYS, LABEVENTS, and PATIENTS tables.
    Focus on key lab tests such as glucose, creatinine, and hemoglobin.
    
    Parameters:
    icustays_file (str): Path to ICUSTAYS.csv.
    labevents_file (str): Path to LABEVENTS.csv.
    patients_file (str): Path to PATIENTS.csv.
    
    Returns:
    pd.DataFrame: Processed dataframe with ICU stay length and lab test values (glucose, creatinine, hemoglobin).
    """
    
    # Load the ICU stays data (ICU stay ID, patient ID, length of stay)
    icustays = pd.read_csv(icustays_file, usecols=['subject_id', 'icustay_id', 'los'])  # 'los' = length of stay
    
    # Load lab events data (subset: glucose, creatinine, hemoglobin)
    labevents = pd.read_csv(labevents_file, usecols=['subject_id', 'itemid', 'charttime', 'value', 'valuenum', 'valueuom'])
    
    # Define relevant ITEMIDs for glucose, creatinine, and hemoglobin within the range 50800-51537
    relevant_itemids = [
        50931,  # Glucose
        50912,  # Creatinine
        51222   # Hemoglobin
    ]
    
    # Filter lab events for the relevant lab tests
    filtered_labevents = labevents[labevents['itemid'].isin(relevant_itemids)]
    
    # Load patient demographic data (for future use, like gender, date of birth)
    patients = pd.read_csv(patients_file, usecols=['subject_id', 'gender', 'dob'])
    
    # Merge the ICU stays data with the filtered lab events
    merged_data = pd.merge(icustays, filtered_labevents, on='subject_id', how='inner')
    
    # Further preprocessing: Convert charttime to datetime for sequential modeling
    merged_data['charttime'] = pd.to_datetime(merged_data['charttime'])
    
    # Merge with patients data to get demographic details (optional)
    merged_data = pd.merge(merged_data, patients, on='subject_id', how='left')
    
    return merged_data

# Example usage
icustays_file = './notebooks/data/ICUSTAYS.csv'
labevents_file = './notebooks/data/LABEVENTS.csv'
patients_file = './notebooks/data/PATIENTS.csv'

mimic_data = load_lab_based_mimic_data(icustays_file, labevents_file, patients_file)
print(mimic_data.head())

mimic_data = pd.DataFrame(mimic_data)

mimic_data.to_csv('./notebooks/data/mimic_data.csv', mode='a', index=False)