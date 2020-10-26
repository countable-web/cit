import csv
import os
import re
import traceback

from pipeline.importers.utils import import_data_into_point_model
from pipeline.models.location_assets import Project
from pipeline.utils import get_quarterly_date_str_as_date

ALTERNATIVE_FIELD_NAMES = {
    "PROJID": "PROJECT_ID",
    "PROJNM": "PROJECT_NAME",
    "PROJTYP": "PROJECT_TYPE",
    "PROJECTTYPE": "PROJECT_TYPE",
    "DESCRIPTION": "PROJECT_DESCRIPTION",
    "DESC": "PROJECT_DESCRIPTION",
    "MUNINM": "MUNICIPALITY",
    "DVLPRNM": "DEVELOPER",
    "INDUSTRY CONSTRUCTION CLASSIFICATION": "CONSTRUCTION_SUBTYPE",
    "ESTCOST ($MILLION)": "ESTIMATED_COST",
    "EST COST ($MILLION)": "ESTIMATED_COST",
    "ESTCOST": "ESTIMATED_COST",
    "EST COST ($MILLION": "ESTIMATED_COST",
    "EST COST (MIL)": "ESTIMATED_COST",
    "STATUS": "PROJECT_STATUS",
    "STAGE": "PROJECT_STAGE",
    "PUBLIC": "PUBLIC_FUNDING_IND",
    "GREEN BUILDING": "GREEN_BUILDING_IND",
    "CLEAN ENERGY": "CLEAN_ENERGY_IND",
    "FIRST_NATION_IND": "INDIGENOUS_IND",
    "FIRST NATION": "INDIGENOUS_IND",
    "FIRST_NATION_NAME": "INDIGENOUS_NAMES",
    "FIRST_NATION_NAMES": "INDIGENOUS_NAMES",
    "FIRST_NATION_AGREEMENT": "INDIGENOUS_AGREEMENT",
    "UPDATE_ACTIVITY": "UPDATED_FIELDS",
    "START DATE": "START_DATE",
    "START": "START_DATE",
    "COMPLETION DATE": "COMPLETION_DATE",
    "COMPL": "COMPLETION_DATE",
    "COMPLETE": "COMPLETION_DATE",
    "FINISH DATE": "COMPLETION_DATE",
    "FINISH": "COMPLETION_DATE",
}

QUARTERS_MAP = {
    "late": "Q4",
    "fall": "Q4",
    "summer": "Q3",
    "spring": "Q2",
    "early": "Q1",
    "dec": "Q4",
    "oct": "Q4",
    "nov": "Q4",
    "sep": "Q3",
    "aug": "Q3",
    "jul": "Q3",
    "jun": "Q2",
    "may": "Q2",
    "apr": "Q2",
    "april": "Q2",
    "mar": "Q1",
    "march": "Q1",
    "feb": "Q1",
    "jan": "Q1",
}

QUARTER_PATTERN = r'^Q[1-4]$'


def import_projects(dir_path):
    directory = os.fsencode(dir_path)

    for file in sorted(os.listdir(directory), reverse=True):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            print("filename", filename)

            with open(os.path.join(dir_path, filename), mode='r', encoding='utf-8-sig', errors='ignore') as f:

                skip_projects_csv_preamble_rows(f, filename)
                reader = csv.DictReader(f)
                data = list(reader)

                for row in data:
                    try:
                        print("row", row)
                        project = normalize_projects_field_names(row)
                        project = handle_projects_fields_edge_cases(project, filename)

                        print("project", project)

                        instance = import_data_into_point_model("projects", Project, project, dry_run=False)
                        print("instance", instance)
                    except Exception as e:
                        print("exception", e)
                        traceback.print_exc()


def skip_projects_csv_preamble_rows(file, filename):
    if int(filename.split("_")[0]) <= 2015:
        for i in range(3):
            file.readline()
            # last_pos = file.tell()
            # line = file.readline()
            # non_null_fields = [field for field in line.strip().split(",") if field != '']
            # if len(non_null_fields) > 10:
            #     break

        # file.seek(last_pos)


def normalize_projects_field_names(row):
    project = {}

    # normalize all field names
    for key in row.keys():
        normalized_key = key.upper().replace(":", "").strip()

        print("key", key, normalized_key)
        # field_names_to_replace = [key for key in row.keys() if key in ALTERNATIVE_FIELD_NAMES]
        # print("field_names_to_replace", field_names_to_replace)
        # for field_name in field_names_to_replace:
        #     field_value = row.pop(field_name)
        #     canonical_field_name = ALTERNATIVE_FIELD_NAMES[field_name.lower()]
        #     row[canonical_field_name] = field_value
        if normalized_key in ALTERNATIVE_FIELD_NAMES:
            normalized_key = ALTERNATIVE_FIELD_NAMES[normalized_key]

        if normalized_key.replace(" ", "_") in ALTERNATIVE_FIELD_NAMES:
            normalized_key = ALTERNATIVE_FIELD_NAMES[normalized_key.replace(" ", "_")]

        normalized_key = normalized_key.replace(" ", "_")

        print("normalized_key", normalized_key)
        project[normalized_key] = row[key]

        # deal with annoying edge cases
        if ":" in project[normalized_key]:
            project[normalized_key] = project[normalized_key].split(":")[-1].strip()

        if project[normalized_key] == '':
            project[normalized_key] = None

    return project


def handle_projects_fields_edge_cases(project, filename):
    if "LAST_UPDATE" not in project.keys():
        project["LAST_UPDATE"] = get_last_update_field_from_filename(filename)

    # TODO clean standardized dates (enforce YYYY-Q[1-4] format)

    if "START_DATE" in project.keys() and "STANDARDIZED_START_DATE" not in project.keys():
        project["STANDARDIZED_START_DATE"] = get_standardized_project_date(project["START_DATE"])

    if "COMPLETION_DATE" in project.keys() and "STANDARDIZED_COMPLETION_DATE" not in project.keys():
        project["STANDARDIZED_COMPLETION_DATE"] = get_standardized_project_date(project["COMPLETION_DATE"])

    NON_NUMERIC = r'[^0-9.]'

    if "LATITUDE" in project.keys() and project["LATITUDE"]:
        project["LATITUDE"] = re.sub(NON_NUMERIC, '', project["LATITUDE"])

    if "LONGITUDE" in project.keys() and project["LONGITUDE"]:
        project["LONGITUDE"] = re.sub(NON_NUMERIC, '', project["LONGITUDE"])

    if "OPERATING_JOBS" in project.keys() and project["OPERATING_JOBS"]:
        project["OPERATING_JOBS"] = re.sub(NON_NUMERIC, '', project["OPERATING_JOBS"])

    if "CONSTRUCTION_JOBS" in project.keys() and project["CONSTRUCTION_JOBS"]:
        project["CONSTRUCTION_JOBS"] = re.sub(NON_NUMERIC, '', project["CONSTRUCTION_JOBS"])

    # if a project is missing the lat/lon columns, try to look for other (more recent) years
    # to see if they contain the lat/lon columns. we import project csv files in reverse
    # chronological order, and older years tend to be missing columns.
    if "LATITUDE" not in project.keys() and "LONGITUDE" not in project.keys():
        existing_projects = Project.objects.filter(
            project_id=project['PROJECT_ID'],
            point__isnull=False)
        if existing_projects:
            print("existing_projects", existing_projects)
            existing_project = existing_projects.first()
            project['LATITUDE'] = existing_project.get_latitude()
            project['LONGITUDE'] = existing_project.get_longitude()
        else:
            project['LATITUDE'] = None
            project['LONGITUDE'] = None

    return project


def get_standardized_project_date(fuzzy_date):
    if not fuzzy_date:
        return None

    match = re.search(r'(.*)(\d{4})$', fuzzy_date)
    if match is None:
        return None

    quarter, year = match.groups()

    # from the data it seems like entries with only a year correspond to Q4
    if not quarter:
        quarter = 'Q4'

    if re.search(QUARTER_PATTERN, quarter):
        quarter_cleaned = quarter
    else:
        quarter_cleaned = QUARTERS_MAP[quarter.strip().lower()] if quarter.strip().lower() in QUARTERS_MAP else None

    if quarter_cleaned:
        return '{}-{}'.format(year, quarter_cleaned)
    else:
        return year


def get_last_update_field_from_filename(filename):
    year, quarter = filename.split(".")[0].split("_")
    quarterly_date_str = "{}-{}".format(year, quarter)
    return get_quarterly_date_str_as_date(quarterly_date_str).strftime("%Y-%m-%d")
