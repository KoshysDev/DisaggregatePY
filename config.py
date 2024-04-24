import os

# Default search rows
default_config = {
    'age_adult_row': 'form.demographics.adding_adult.hh_adult.list_for_adult.repeated_data2.age_adult',
    'gender_adult_row': 'form.demographics.adding_adult.hh_adult.list_for_adult.repeated_data2.gender_list_adult',
    'dis_adult_row': 'form.demographics.adding_adult.hh_adult.list_for_adult.repeated_data2.disability',
    'age_child_row': 'form.demographics.adding_child.hh_childs.list_for_child.repeated_data.age_child',
    'gender_child_row': 'form.demographics.adding_child.hh_childs.list_for_child.repeated_data.gender_list_child',
    'dis_child_row': 'form.demographics.adding_child.hh_childs.list_for_child.repeated_data.disability',
    'age_app_row': 'form.demographics.age',
    'gender_app_row': 'form.demographics.gender',
    'form_app_number': 'number',
    'hh_size_app_row': 'form.demographics.hh_size',
    'low_app_income': 'form.demographics.low_income',
    'hh_idp_app_row': 'form.demographics.HH_hosting_IDPs',
    'idp_app_row': 'form.demographics.IDP',
    'child_count_app_row': 'form.demographics.adding_child.count_of_children',
    'dis_app_row': 'form.demographics.main_recipient_disability',
}

# Function to create config file if it doesn't exist
def create_config_file(filename="config.json"):
    if not os.path.exists(filename):
        import json
        with open(filename, 'w') as f:
            json.dump(default_config, f, indent=4)