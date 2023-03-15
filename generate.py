import pandas as pd
from datetime import datetime, timedelta
import random
from faker import Faker

def generate_names(num, gender):
    fake = Faker()
    Faker.seed(0)  # for reproducibility
    names = []
    surnames = []
    while len(names) < num:
        if gender.lower() == 'male':
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
        elif gender.lower() == 'female':
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()
        else:
            raise ValueError('Invalid gender: choose either "male" or "female"')
        full_name = f"{first_name} {last_name}"
        if full_name not in [f"{n} {s}" for n, s in zip(names, surnames)]:
            names.append(first_name)
            surnames.append(last_name)
    df = pd.DataFrame({'first name': names, 'last name': surnames, 'gender':gender})
    return df

def generate_dob_column(num_rows, age_ranges, as_of_date=None):
    if not as_of_date:
        as_of_date = datetime.today()
    total_percentage = sum(age_ranges.values())
    if total_percentage != 100:
        raise ValueError(f'Percentages in age ranges dictionary must add up to 100. Current total is {total_percentage}.')
    dob_list = []
    for age_range, percentage in age_ranges.items():
        num_people = round(num_rows * percentage / 100)
        start_age = age_range[0]
        end_age = age_range[1]
        for i in range(num_people):
            age = random.randint(start_age, end_age)
            birth_year = as_of_date.year - age
            birth_date = datetime(birth_year, 1, 1) + timedelta(days=random.randint(0, 364))
            dob_list.append(birth_date)
    df = pd.DataFrame({'date of birth': dob_list})
    return df

def calc_age_column(df, dob_column_name='date of birth', as_of_date=None):
    if as_of_date is None:
        as_of_date = datetime.today()
    else:
        as_of_date = pd.to_datetime(as_of_date)
    df['age'] = as_of_date.year - df[dob_column_name].dt.year - ((as_of_date.date() < (df[dob_column_name] + pd.offsets.YearEnd()).dt.date) & (as_of_date.month < df[dob_column_name].dt.month))
    return df

def create_random_names(num,gender,age_ranges,as_of_date=None):
    a = generate_names(num,gender)
    b = generate_dob_column(num,age_ranges)
    c = pd.concat([a, b], axis=1)
    return c

def create_dataset(num_males,num_females,m_age_ranges,f_age_ranges,as_of_date=None):
    m_names = create_random_names(num_males, 'male',m_age_ranges,as_of_date=as_of_date)
    f_names = create_random_names(num_females, 'female',f_age_ranges,as_of_date=as_of_date)
    data = pd.concat([f_names,m_names]).reset_index(drop=True)
    data = data.sample(frac=1).reset_index(drop=True)
    return data