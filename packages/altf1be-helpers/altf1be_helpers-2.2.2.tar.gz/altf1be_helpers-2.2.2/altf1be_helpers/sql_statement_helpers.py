

from ..models.html_head import Base, LeseshopsbelgesItem
from sqlalchemy import engine
from sqlalchemy.orm.session import sessionmaker
from altf1be_helpers import get_logger
logger = get_logger()


class SQLstatementsHelper():

    session = None
    engine = None
    s = None
    cursor = None
    rows=None
    def __init__(self, database_uri, object_type):
        self.engine = engine.create_engine(database_uri)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def __del__(self):
        self.session.close()
        
    def get_cursor(self, select, table):
        self.cursor = None
        with self.engine.connect() as connection:
            self.cursor = connection.execute(
                f'select {",".join(select)} from {table}')
            self.rows = self.cursor.fetchall()
            for row in self.rows:
                logger.info(f"row: {row}")
        return self.cursor.returns_rows

    def insert_row_in_items(self, item):
        logger.info('create a new item in items')
        item_to_store = LeseshopsbelgesItem(
            category="".join(item['category']),
            name="".join(item['name']),
            url="".join(item['url']),
            description="".join(item['description']),
            http_status=item['http_status'][0]
        )

        self.session.add(item_to_store)
        self.session.commit()
