"""Initial migration

Revision ID: 7e338fc0f8cf
Revises: 
Create Date: 2024-02-24 01:16:30.644124

"""

from typing import Sequence, Union
import uuid

from alembic import op
import bcrypt
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = "7e338fc0f8cf"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create all tables
    op.create_table(
        "predavanja",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("predmet_id", UUID(as_uuid=True), nullable=False),
        sa.Column("broj_predavanja", sa.Integer, nullable=False),
        sa.Column("qrcode", sa.String),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("datumPredavanja", sa.Date, nullable=False),
    )

    op.create_table(
        "predavanja_korisnici",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("predavanje_id", UUID(as_uuid=True), nullable=False),
        sa.Column("korisnik_id", UUID(as_uuid=True), nullable=False),
        sa.Column("ime_prezime", sa.String),
        sa.Column("naziv_predavanja", sa.String),
    )

    op.create_table(
        "predmeti",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("naziv", sa.String, nullable=False),
        sa.Column("godina_studija", sa.Integer),
    )

    op.create_table(
        "predmeti_korisnici",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("predmet_id", UUID(as_uuid=True), nullable=False),
        sa.Column("korisnik_id", UUID(as_uuid=True), nullable=False),
        sa.Column("ime_prezime", sa.String),
        sa.Column("naziv_predmeta", sa.String),
        sa.Column("role", sa.String, nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("date_of_birth", sa.Date),
        sa.Column("password", sa.String),
        sa.Column("role", sa.String),
    )

    # Add foreign key constraints
    op.create_foreign_key(
        "predavanja_predmet_id_fkey", "predavanja", "predmeti", ["predmet_id"], ["id"]
    )
    op.create_foreign_key(
        "predavanja_korisnici_korisnik_id_fkey",
        "predavanja_korisnici",
        "users",
        ["korisnik_id"],
        ["id"],
    )
    op.create_foreign_key(
        "predavanja_korisnici_predavanje_id_fkey",
        "predavanja_korisnici",
        "predavanja",
        ["predavanje_id"],
        ["id"],
    )
    op.create_foreign_key(
        "predmeti_korisnici_korisnik_id_fkey",
        "predmeti_korisnici",
        "users",
        ["korisnik_id"],
        ["id"],
    )
    op.create_foreign_key(
        "predmeti_korisnici_predmet_id_fkey",
        "predmeti_korisnici",
        "predmeti",
        ["predmet_id"],
        ["id"],
    )


def downgrade():
    # Drop foreign keys in reverse order first
    op.drop_constraint(
        "predmeti_korisnici_predmet_id_fkey", "predmeti_korisnici", type_="foreignkey"
    )
    op.drop_constraint(
        "predmeti_korisnici_korisnik_id_fkey", "predmeti_korisnici", type_="foreignkey"
    )
    op.drop_constraint(
        "predavanja_korisnici_predavanje_id_fkey",
        "predavanja_korisnici",
        type_="foreignkey",
    )
    op.drop_constraint(
        "predavanja_korisnici_korisnik_id_fkey",
        "predavanja_korisnici",
        type_="foreignkey",
    )
    op.drop_constraint("predavanja_predmet_id_fkey", "predavanja", type_="foreignkey")

    # Drop tables
    op.drop_table("users")
    op.drop_table("predmeti_korisnici")
    op.drop_table("predmeti")
    op.drop_table("predavanja_korisnici")
    op.drop_table("predavanja")
    # ### end Alembic commands ###
