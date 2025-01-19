from backend.db import dbconn
from . import resume_info
from . import standard_section


class DBFetch:
    """
    DBFetch class to fetch data from the database
    """

    def __init__(self) -> None:
        """
        Initialize the database connection
        """
        self.database = dbconn.DBConn()

    def fetch_all(
        self, user_id: int, section_selectons: list[str]
    ) -> resume_info.FullResumeInfo:
        """
        Fetch user details from the database
        """
        sql_query = f"""
        SELECT s.*
        FROM user_table u
        JOIN LATERAL UNNEST(u.rsid_list) AS u_rsid ON true
        JOIN sections s ON s.rsid = u_rsid
        WHERE u.uid = '{user_id}';
        """
        user = self.database.run_sql(sql_query)
        stand_sect_list = []
        for section in user:
            target_item_type = section["sect_type"]
            item_list = section["item_list"]
            item_info_list = []
            print("DEBUG: item_list")
            print(item_list)
            for item_id in item_list:
                fetch_item_query = f"""
                SELECT r.*
                FROM resume_item r
                WHERE iid = {item_id};
                """
                item_info_raw = self.database.run_sql(fetch_item_query)
                item_info = item_info_raw[0]
                print(item_info)
                if item_info["item_type"] == target_item_type:
                    item_info_list.append(
                        [
                            item_info["header_list"],
                            item_info["contents"],
                            item_info["item_attributes"],
                        ]
                    )
                else:
                    print("Error: item type does not match")
            stand_sect_list.append(
                standard_section.SectInfo(
                    section["header_name"], item_info_list, section["sect_type"]
                )
            )
            # Defaulting bullet point to be true, change in frontend if needed
        del self.database
        return resume_info.FullResumeInfo(section_selectons, stand_sect_list)
