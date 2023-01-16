"""UUID generation

Revision ID: 92cc120d7301
Revises:
Create Date: 2023-01-15 15:52:38.909719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "92cc120d7301"
down_revision = None
branch_labels = None
depends_on = None


# uuid_generate_v7 and uuid_generate_v8 code copied from this gist
# https://gist.github.com/kjmph/5bd772b2c2df145aa645b837da7eca74

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("""
        create or replace function uuid_generate_v7()
        returns uuid
        as $$
        declare
          unix_ts_ms bytea;
          uuid_bytes bytea;
        begin
          unix_ts_ms = substring(int8send(floor(extract(epoch from clock_timestamp()) * 1000)::bigint) from 3);
        
          -- use random v4 uuid as starting point (which has the same variant we need)
          uuid_bytes = uuid_send(gen_random_uuid());
        
          -- overlay timestamp
          uuid_bytes = overlay(uuid_bytes placing unix_ts_ms from 1 for 6);
        
          -- set version 7
          uuid_bytes = set_byte(uuid_bytes, 6, (b'0111' || get_byte(uuid_bytes, 6)::bit(4))::bit(8)::int);
        
          return encode(uuid_bytes, 'hex')::uuid;
        end
        $$
        language plpgsql
        volatile;
    """)
    op.execute("""
        -- Generate a custom UUID v8 with microsecond precision
        create or replace function uuid_generate_v8()
        returns uuid
        as $$
        declare
          unix_ts_ms bytea;
          uuid_bytes bytea;
          timestamp    timestamptz;
          microseconds int;
        begin
          timestamp    = clock_timestamp();
          unix_ts_ms = substring(int8send(floor(extract(epoch from timestamp) * 1000)::bigint) from 3);
          microseconds = (cast(extract(microseconds from timestamp)::int - (floor(extract(milliseconds from timestamp))::int * 1000) as double precision) * 4.096)::int;
        
          -- use random v4 uuid as starting point (which has the same variant we need)
          uuid_bytes = uuid_send(gen_random_uuid());
        
          -- overlay timestamp
          uuid_bytes = overlay(uuid_bytes placing unix_ts_ms from 1 for 6);
        
          -- set version 8
          uuid_bytes = set_byte(uuid_bytes, 6, (b'1000' || (microseconds >> 8)::bit(4))::bit(8)::int);
          uuid_bytes = set_byte(uuid_bytes, 7, microseconds::bit(8)::int);
        
          return encode(uuid_bytes, 'hex')::uuid;
        end
        $$
        language plpgsql
        volatile;
    """)


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\"")
    op.execute("DROP FUNCTION uuid_generate_v7()")
    op.execute("DROP FUNCTION uuid_generate_v8()")
