import pandas as pd

def find_section_pos(section_csv, section_ranges, csv_out=None):
    """A function to find all the sections in a section csv between a specified range of words or characters
    Used to help read a graph - where there is a sharp increase in mentions we might want to retrieve the section
    names corresponding to that part of the graph"""
    section_df = pd.read_csv(section_csv)
    
    df_out = pd.DataFrame()
    for section_range in section_ranges:
        filtered_df = section_df[section_df["mid_pos"].between(section_range[0], section_range[1])]
        filtered_df["start"] = section_range[0]
        filtered_df["end"] = section_range[1]
        df_out = pd.concat([df_out, filtered_df])
    
    df_out = df_out.sort_values(by=["start"])

    if csv_out is not None:
        df_out.to_csv(csv_out, encoding='utf-8-sig', index=False)

    return df_out

if __name__ == "__main__":
    section_csv = "C:/Users/mathe/Documents/Github-repos/fitna-study/release-08-09-2022/dates_data/0845Maqrizi.Mawaciz.MAB02082022.sections-top10-dates.csv"
    section_ranges = [[400000, 500000],
                      [350000, 400000],
                      [220000, 280000],
                      [550000, 600000]]
    csv_out = "0845Maqrizi.Mawaciz.MAB02082022.sections-top10-dates.filtered-date-ranges.csv"
    find_section_pos(section_csv, section_ranges, csv_out)