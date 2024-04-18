from datetime import datetime
from util import test_history_migration
from database import supabase_middleman



if __name__ == "__main__":
    test_history_migration.test_migrate_history_middle_day(datetime.now(), True)
