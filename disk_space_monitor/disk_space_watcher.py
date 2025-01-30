# - IMPORTS -------------------------------------------------------------------
import pandas as pd


# - CLASSES -------------------------------------------------------------------
class DiskSPaceWatcher:
    def __init__(self):
        self.df = None
        self.header = [
            "Filesystem",
            "Size",
            "Used",
            "Avail",
            "Use%",
            "Mounted",
        ]

    def parse_df_output(self, cmd_output):
        """Parse the cmd output into a DataFrame."""
        lines = cmd_output[0].strip().split("\n")
        data = [line.split(maxsplit=5) for line in lines]

        self.df = pd.DataFrame(data, columns=self.header)

    def clean_and_process_data(self):
        """Clean and process the DataFrame for numeric operations."""
        if self.df is None:
            raise ValueError(
                "No data to process. Run parse_df_output() first."
            )

        try:
            self.df["Use%"] = self.df["Use%"].str.rstrip("%").astype(int)
            self.relevant_df = self.df.loc[:, "Size":"Use%"].astype(int)
        except:
            pass

    def calculate_totals_and_averages(self):
        """Calculate totals and averages."""
        totals = self.relevant_df.sum(axis=0)
        averages = self.relevant_df.mean(axis=0)

        return totals, averages

    @staticmethod
    def convert_into_human_readable_form(kb_size):
        """Convert KB size into MB, GB, and TB."""
        next_unit_by = 1024
        mb_size = round(kb_size / (next_unit_by), 2)
        gb_size = round(kb_size / (next_unit_by**2), 2)
        tb_size = round(kb_size / (next_unit_by**3), 2)

        return {"KB": kb_size, "MB": mb_size, "GB": gb_size, "TB": tb_size}

    def get_disk_space_statistics(self, cmd_output):
        # print(cmd_output)
        self.parse_df_output(cmd_output)
        self.clean_and_process_data()
        totals, averages = self.calculate_totals_and_averages()
        key = "TB"
        condenced_info = {
            "dataframe": self.relevant_df,
            "Tot Size": self.convert_into_human_readable_form(totals[0])[key],
            "Tot Used": self.convert_into_human_readable_form(totals[1])[key],
            "Tot Avail": self.convert_into_human_readable_form(totals[2])[key],
            "Avg Use %": averages[-1],
        }

        return condenced_info


# - TEST ----------------------------------------------------------------------
if __name__ == "__main__":
    cmd_output = """
    /dev/sdd2       671741352  546784456  90760828  86% /
    /dev/sda       6200273136 5748856820 138865304  98% /mnt/SSD1-6TB
    /dev/sdb       6200273136 5423601752 464120372  93% /mnt/SSD2-6TB
    /dev/sdc       6200273136 5766142956 121579168  98% /mnt/SSD3-6TB
    """

    # Instantiate the extractor
    extractor = DiskSPaceWatcher()

    # Parse the `df` output
    extractor.parse_df_output(cmd_output)
    print("Initial DataFrame:")
    print(extractor.df)

    # Clean and process the data
    relevant_df = extractor.clean_and_process_data()
    print("\nRelevant DataFrame (Cleaned):")
    print(relevant_df)

    # Calculate totals and averages
    totals, averages = extractor.calculate_totals_and_averages()
    print("\nTotal Space Information:")
    print(totals)
    print("\nAverage Space Information:")
    print(averages)

    # Convert totals to human-readable form
    print(
        "\nTotal Server Size (Human Readable):",
        extractor.convert_into_human_readable_form(totals["Size"]),
    )
    print(
        "Total Server Used Space (Human Readable):",
        extractor.convert_into_human_readable_form(totals["Used"]),
    )
    print(
        "Total Server Available Space (Human Readable):",
        extractor.convert_into_human_readable_form(totals["Avail"]),
    )
