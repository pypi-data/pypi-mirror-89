import logging

from pegaflow.db.admin.admin_loader import *
from pegaflow.db.admin.versions.base_version import BaseVersion
from pegaflow.db.schema import *
from sqlalchemy.exc import *

DB_VERSION = 11

log = logging.getLogger(__name__)


class Version(BaseVersion):
    def __init__(self, connection):
        super(Version, self).__init__(connection)

    def update(self, force=False):
        """

        :param force:
        :return:
        """
        log.info('Updating to version %s' % DB_VERSION)
        try:
            log.debug('Renaming integrity_metrics table...')
            if self.db.get_bind().driver == "mysqldb":
                self.db.execute('RENAME TABLE integrity_metrics TO integrity')
            else:
                self.db.execute('ALTER TABLE integrity_metrics RENAME TO integrity')

        except (OperationalError, ProgrammingError):
            pass
        except Exception as e:
            self.db.rollback()
            log.exception(e)
            raise Exception(e)

        self.db.commit()

    def downgrade(self, force=False):
        """

        """
        log.info('Downgrading from version %s' % DB_VERSION)
        try:
            log.debug('Renaming integrity table...')
            if self.db.get_bind().driver == "mysqldb":
                self.db.execute('RENAME TABLE integrity TO integrity_metrics')
            else:
                self.db.execute('ALTER TABLE integrity RENAME TO integrity_metrics')
        except (OperationalError, ProgrammingError):
            pass
        except Exception as e:
            self.db.rollback()
            log.exception(e)
            raise Exception(e)

        self.db.commit()
