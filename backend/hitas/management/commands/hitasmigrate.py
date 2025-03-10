import os
import sys

import cx_Oracle
from django.core.management.base import BaseCommand, CommandParser

from hitas.models import MigrationDone


class Command(BaseCommand):
    help = "Hitas database migration tool."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--skip-anonymize", action="store_true", help="Skip creating anonymous data.")
        parser.add_argument("--debug", action="store_true", help="Show debug information.")
        parser.add_argument(
            "--truncate", action="store_true", help="Truncate hitas tables before starting the migration."
        )
        parser.add_argument("--truncate-only", action="store_true", help="Truncate hitas tables and quits.")
        parser.add_argument("--check", action="store_true", help="Checks only if database migration has been done.")
        parser.add_argument("--oracle-host", default="localhost", help="Oracle database host (default: 'localhost').")
        parser.add_argument("--oracle-port", type=int, default=1521, help="Oracle database port (default: 1521).")
        parser.add_argument("--oracle-user", default="system", help="Oracle database user (default: 'system').")
        parser.add_argument(
            "--oracle-password",
            default="oracle",
            help="Oracle database password (default 'oracle')."
            " Can be also set with 'HITAS_ORACLE_PASSWORD' environment variable.",
        )
        # MacOS only:
        # Before you can run the migration, you will need to install oracle instantclient:
        # https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#scripted-installation
        parser.add_argument(
            "--oracle-instantclient-path",
            default="Downloads/instantclient_19_8",
            help="Oracle instantclient location, MacOS only (default: 'Downloads/instantclient_19_8').",
        )
        parser.add_argument(
            "--minimal-dataset",
            action="store_true",
            help="Only migrate a pre-specified set of housing companies e.g. for a testing environment",
        )

    def handle(self, *args, **options) -> None:
        if sys.platform.startswith("darwin"):  # MacOS
            try:
                lib_dir = os.path.join(os.environ.get("HOME"), options["oracle_instantclient_path"])
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            except Exception as err:
                print(err)
                return

        try:
            oracle_pw = os.environ["HITAS_ORACLE_PASSWORD"]
        except KeyError:
            oracle_pw = options["oracle_password"]

        if MigrationDone.objects.first() and not (options["truncate"] or options["truncate_only"]):
            print("Migration already done...")
            exit(1)
        if options["check"]:
            return

        # Import migration runner here so its dependencies (like sqlalchemy) are not required for a simple
        # check if migration is done
        from hitas.oracle_migration.runner import run

        run(
            options["oracle_host"],
            options["oracle_port"],
            options["oracle_user"],
            oracle_pw,
            options["debug"],
            not options["skip_anonymize"],
            options["truncate"],
            options["truncate_only"],
            options["minimal_dataset"],
        )
