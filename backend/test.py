"""Used to run simple tests against the database locally"""

from datetime import datetime

from util import test_history_migration

if __name__ == "__main__":
    test_history_migration.test_migrate_history_middle_day(datetime.now(), True)
    test_history_migration.test_migrate_history_end_of_day(datetime.now(), True)
