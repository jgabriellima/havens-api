from sqlalchemy import Column, String, ForeignKey, Table
from api_template.db.base import Base

# Tabela de associação
client_assistant_association = Table(
    'client_assistant_association',
    Base.metadata,
    Column('client_id', String, ForeignKey('clients.id', ondelete='CASCADE'), primary_key=True),
    Column('assistant_id', String, ForeignKey('assistants.id', ondelete='CASCADE'), primary_key=True)
) 