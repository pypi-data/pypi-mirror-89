# Perseus MicrORM

Majormode Perseus MicrORM Python Library is a small, little, mini, tiny, micro Object-Relational Mapping (ORM).

MicrORM is not a object-relational mapping in the sense it maps Pyth objects to a Relational DataBase Management System (RDBMS), but in the sense it maps results of SQL queries, executed on a RDBMS, to Python objects.

## Installation

To install [Perseus MicrORM Python Library](https://github.com/dcaune/perseus-microrm-python-library), simply enter the follow command line:

``` shell
pip install perseus-microrm-library
```

## Usage

``` python
import uuid

from majormode.perseus.utils import cast
from majormode.perseus.utils.rdbms import RdbmsConnection


RDBMS_CONNECTION_PROPERTIES = {
    None: {
        'rdbms_hostname': 'localhost',
        'rdbms_port': 5432,
        'rdbms_database_name': 'foo',
        'rdbms_account_username': 'dbo',
        'rdbms_account_password': ''
    }
}

PLACE_IDS = [
    uuid.UUID('54879ffc-a1ec-11e8-85bd-0008a20c190f'),
    uuid.UUID('9025d1c8-a1ec-11e8-9e29-0007cb040bcc')
]

with RdbmsConnection.acquire_connection(
        RDBMS_CONNECTION_PROPERTIES,
        auto_commit=False,
        connection=None) as connection:
    cursor = connection.execute(
        """
        SELECT place_id,
               ST_X(location) AS longitude,
               ST_Y(location) AS latitude,
               ST_Z(location) AS altitude,
               accuracy,
               creation_time
          FROM place
          WHERE place_id IN %[place_ids]s
        """,
        {
            'place_ids': PLACE_IDS 
        })
    rows = cursor.fetch_all()

    places = [
        row.get_object({
            'place_id': cast.string_to_uuid,
            'creation_time': cast.string_to_timestamp})
        for row in cursor.fetch_all()]

    for place in places:
        print(place.place_id, place.longitude, place.latitude)
```
